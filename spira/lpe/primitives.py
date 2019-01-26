import gdspy
import numpy as np
import networkx as nx
from demo.pdks import ply

from copy import copy, deepcopy
from spira import settings

import spira
from spira import param
from spira import settings
from spira.gdsii import utils
from spira.rdd import get_rule_deck

from spira.gdsii.cell import Cell
from spira.gdsii.layer import Layer
from spira.gdsii.elemental.polygons import Polygons
from spira.gdsii.elemental.label import Label
from spira.gdsii.elemental.port import Port
from spira.gdsii.elemental.sref import SRef
from spira.lne.graph import Graph
from spira.core.lists import ElementList

from spira.lpe.layers import *
from spira.lpe.structure import __ConstructLayers__
from spira.lpe.containers import __CellContainer__
from spira.lpe import mask
from spira.lne.net import Net


RDD = get_rule_deck()


class __Layout__(__ConstructLayers__):

    level = param.IntegerField(default=1)
    lcar = param.IntegerField(default=0.1)
    algorithm = param.IntegerField(default=6)

    primitives = param.DataField(fdef_name='create_primitives')

    def create_elementals(self, elems):
        super().create_elementals(elems)
        return elems

    def create_primitives(self):
        ports = self.ports
        elems = self.elementals
        prim_elems = ElementList()
        for S in elems.sref:
            if isinstance(S.ref, mask.Native):
                for N in S.ref.elementals:
                    prim_elems += N
        if ports is not None:
            for P in ports:
                prim_elems += P
        return prim_elems

    def get_metal_polygons(self, pl):
        elems = self.elementals
        ply_elems = ElementList()
        for S in elems.sref:
            if isinstance(S.ref, mask.Metal):
                for M in S.ref.elementals:
                    if M.layer.is_equal_number(pl.layer):
                        if M.polygon.gdslayer.datatype in (1, 2):
                            ply_elems += M.polygon
        return ply_elems

    def create_nets(self, nets):
        for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            metal_elems = self.get_metal_polygons(pl)
            if metal_elems:
                net = Net(
                    name='{}'.format(pl.layer.number),
                    lcar=self.lcar,
                    level=self.level,
                    algorithm=self.algorithm,
                    layer=pl.layer,
                    polygons=metal_elems,
                    primitives=self.primitives,
                    bounding_boxes=self.bounding_boxes
                )
                nets += net.graph
        return nets


class Device(__Layout__):

    def create_netlist(self):
        self.g = self.merge
        self.g = self.nodes_combine(algorithm='d2d')
        self.g = self.nodes_combine(algorithm='s2s')

        if self.g is not None:
            for n in self.g.nodes():
                # self.g.node[n]['pos'] += self.midpoint
                self.g.node[n]['surface'].node_id = '{}_{}'.format(self.name, self.g.node[n]['surface'].node_id)
                if 'device' in self.g.node[n]:
                    self.g.node[n]['device'].node_id = '{}_{}'.format(self.name, self.g.node[n]['device'].node_id)

        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')

        return self.g


class Gate(__Layout__):

    original = param.CellField()
    devices = param.CellField()

    get_device_refs = param.DataField(fdef_name='create_get_device_references')
    device_ports = param.DataField(fdef_name='create_device_ports')
    terminals = param.DataField(fdef_name='create_terminals')

    def create_get_device_references(self):
        elems = spira.ElementList()
        for e in self.devices.elementals.sref:
            elems += e
        return elems

    def create_terminals(self):
        ports = spira.ElementList()
        flat_elems = self.original.elementals.flat_copy()
        port_elems = flat_elems.get_polygons(layer=RDD.PURPOSE.TERM)
        label_elems = flat_elems.labels

        for port in port_elems:
            for label in label_elems:

                lbls = label.text.split(' ')
                s_p1, s_p2 = lbls[1], lbls[2]
                p1, p2 = None, None

                for m1 in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
                    if m1.layer.name == s_p1:
                        p1 = spira.Layer(name=lbls[0], 
                            number=m1.layer.number, 
                            datatype=RDD.GDSII.TEXT
                        )
                        if label.point_inside(ply=port.polygons[0]):
                            ports += spira.Term(
                                name=lbls[0],
                                layer1=p1,
                                midpoint=label.position,
                                width=port.dx,
                                length=port.dy
                            )
                    if m1.layer.name == s_p2:
                        p2 = spira.Layer(name=lbls[0], 
                            number=m1.layer.number, 
                            datatype=RDD.GDSII.TEXT
                        )
                        if label.point_inside(ply=port.polygons[0]):
                            ports += spira.Term(
                                name=lbls[1],
                                layer2=p2,
                                midpoint=label.position,
                                width=port.dy
                            )
        return ports

    def create_device_ports(self):
        ports = spira.ElementList()
        for g in self.original.elementals.polygons:
            for D in self.devices.elementals.sref:
                for S in D.ref.elementals:
                    if isinstance(S.ref, mask.Metal):
                        for M in S.ref.elementals:
                            if (M.polygon & g) and (g.is_equal_layers(M.polygon)):
                                P = M.metal_port._copy()
                                P.connect(D, M.polygon)
                                d = M.polygon.center + D.midpoint
                                P.move(midpoint=P.midpoint, destination=d)
                                ports += P
        return ports

    def create_ports(self, ports):
        for p in self.device_ports:
            ports += p
        for p in self.terminals:
            ports += p
        return ports

    def create_netlist(self):
        self.g = self.merge
        self.g = self.nodes_combine(algorithm='d2d')
        # self.g = self.generate_paths
        # self.g = self.nodes_combine(algorithm='s2s')
        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')
        return self.g


class BoundingDevice(__CellContainer__):
    """ Add a GROUND bbox to Device for primitive and DRC 
    detection, since GROUND is only in Mask Cell. """
    def create_elementals(self, elems):
        setter = {}
        for p in self.cell.elementals.polygons:
            layer = p.gdslayer.number
            setter[layer] = 'not_set'
        for p in self.cell.elementals.polygons:
            for pl in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
                if pl.layer == p.gdslayer:
                    if setter[pl.layer.number] == 'not_set':
                        l1 = Layer(name='BoundingBox', number=pl.layer.number, datatype=9)
                        ply = Polygons(shape=self.cell.pbox, gdslayer=l1)
                        ply.center = (0,0)
                        elems += ply
                        setter[pl.layer.number] = 'already_set'
        return elems


class __Generator__(__CellContainer__):

    generate_devices = param.DataField(fdef_name='create_devices')

    level = param.IntegerField(default=1)

    def create_device_layers(self):
        c2dmap = {}
        dev = deepcopy(self.cell)
        deps = dev.dependencies()
        for key in RDD.DEVICES.keys:
            for C in deps:
                B = BoundingDevice(cell=C)
                c2dmap.update({C: B})
        for c in dev.dependencies():
            self.w2c(c, c2dmap)
        return SRef(dev)

    def w2n(self, new_cell, c, c2dmap):
        for e in c.elementals:
            if isinstance(e, SRef):
                S = deepcopy(e)
                if e.ref in c2dmap:
                    S.ref = c2dmap[e.ref]
                    # e.ref = c2dmap[e.ref]
                    new_cell += S
                # new_cell += e

    def w2c(self, c, c2dmap):
        for e in c.elementals:
            if isinstance(e, SRef):
                if e.ref in c2dmap:
                    e.ref = c2dmap[e.ref]

    def create_devices(self):
        deps = self.cell.dependencies()
        c2dmap = {}
        for key in RDD.DEVICES.keys:
            DeviceTCell = RDD.DEVICES[key].PCELL
            for C in deps:
                D = Device(cell=C, cell_elems=C.elementals, level=1, lcar=0.01)
                for P in DeviceTCell.elementals.sref:
                    P.ref.create_elementals(D.elementals)
                c2dmap.update({C: D})

        devices = spira.Cell(name='Devices')
        for c in self.cell.dependencies():
            self.w2n(devices, c, c2dmap)

        return devices

    def create_gates(self):
        dev = self.create_device_layers()

        gate = Gate(
            original=self.cell,
            devices=self.generate_devices,
            cell=dev.ref,
            cell_elems=dev.ref.elementals,
            level=2, lcar=0.1
        )

        return gate


class Layout(spira.Cell):
    """  """

    gate = param.CellField()

    def create_elementals(self, elems):
        super().create_elementals(elems)
        elems += spira.SRef(self.gate)
        for e in self.gate.get_device_refs:
            elems += e
        return elems

    def create_nets(self, nets):
        for s in self.elementals.sref:
            g = s.ref.netlist
            if g is not None:
                for n in g.nodes():
                    p = np.array(g.node[n]['pos'])
                    m = np.array(s.midpoint)
                    g.node[n]['pos'] = p + m
                nets += g
        return nets

    def create_netlist(self):
        self.g = self.merge
        self.g = self.nodes_combine(algorithm='d2s')
        # self.g = self.nodes_combine(algorithm='d2d')
        # self.g = self.nodes_combine(algorithm='s2s')

        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')


class GateGenerator(__Generator__):
    """
    Connect to the current library and get the
    primitive metadata from the Rule Deck.
    The pcell device is updated after parsing the
    elementals in the via pcell class.
    """

    structure_gate = param.DataField(fdef_name='create_structure_gate')

    def create_structure_gate(self):

        L = Layout(
            gate=self.create_gates()
        )

        L.netlist

        return SRef(L)


class SLayout(GateGenerator):
    """ The StructureLayout is a converted layout
    that takes designed elementals and wraps them
    with different generators.

    Examples
    --------
    >>> sl = SLayout()
    """

    def create_elementals(self, elems):

        # Primitives
        if self.level == 0:
            elems += SRef(self.cell)
        # Devices
        elif self.level == 1:
            elems += self.generate_devices
        # Gates
        elif self.level == 2:
            elems += self.structure_gate
        # Circuits
        elif self.level == 3:
            elems += self.structure_circuit
        # Mask
        elif self.level == 4:
            elems += self.structure_mask

        return elems








