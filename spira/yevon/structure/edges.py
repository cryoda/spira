import numpy as np

from copy import deepcopy
from spira.yevon.gdsii.group import Group
from spira.core.transforms import *
from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.gdsii.polygon import Box, Polygon
from spira.yevon.geometry.coord import Coord
from spira.yevon.gdsii.base import __LayerElemental__
from spira.core.parameters.descriptor import DataField
from spira.core.parameters.variables import *
from spira.yevon.process import get_rule_deck


__all__ = ['Edge', 'EdgeList', 'EdgeEuclidean', 'EdgeSquare', 'EdgeSideExtend']


RDD = get_rule_deck()


def generate_polygon_edges(shape, layer):
    """ Generates edge objects for each shape segment. """

    xpts = list(shape.x_coords)
    ypts = list(shape.y_coords)

    n = len(xpts)
    xpts.append(xpts[0])
    ypts.append(ypts[0])

    clockwise = 0
    for i in range(0, n):
        clockwise += ((xpts[i+1] - xpts[i]) * (ypts[i+1] + ypts[i]))

    if layer.name == 'BBOX': bbox = True
    else: bbox = False

    edges = ElementalList()
    for i in range(0, n):

        name = '{}_e{}'.format(layer.name, i)
        x = np.sign(clockwise) * (xpts[i+1] - xpts[i])
        y = np.sign(clockwise) * (ypts[i] - ypts[i+1])
        orientation = (np.arctan2(x, y) * constants.RAD2DEG)
        midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
        width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))

        layer = RDD.GDSII.IMPORT_LAYER_MAP[layer]
        inward_extend = RDD[layer.process.symbol].MIN_SIZE / 2
        outward_extend = RDD[layer.process.symbol].MIN_SIZE / 2
        edge = Edge(width=width, inward_extend=inward_extend, outward_extend=outward_extend, layer=layer)

        T = Rotation(orientation+90) + Translation(midpoint)
        edge.transform(T)
        edges += edge

    return edges


class __Edge__(Group, __LayerElemental__):

    width = NumberField(default=1)
    inward_extend = NumberField(default=1)

    inside_edge_layer = DataField(fdef_name='create_inside_edge_layer')
    inside = DataField(fdef_name='create_inside')

    def create_inside_edge_layer(self):
        layer = deepcopy(self.layer)
        layer.purpose = RDD.PURPOSE.PORT.INSIDE
        return layer

    def create_inside(self):
        c2 = Coord(0, self.inward_extend/2)
        ply = Box(alias='InsideEdge', width=self.width, height=self.inward_extend, center=c2, layer=self.inside_edge_layer)
        return ply


class Edge(__Edge__):

    pid = StringField(default='no_pid')
    outward_extend = NumberField(default=1)

    outside = DataField(fdef_name='create_outside')
    outside_edge_layer = DataField(fdef_name='create_outside_edge_layer')

    def create_outside_edge_layer(self):
        layer = deepcopy(self.layer)
        layer.purpose = RDD.PURPOSE.PORT.OUTSIDE
        return layer

    def create_outside(self):
        c1 = Coord(0, -self.outward_extend/2)
        ply = Box(alias='OutsideEdge', width=self.width, height=self.outward_extend, center=c1, layer=self.outside_edge_layer)
        return ply
        
    def overlaps(self, other):
        """ Returns `True` if the edge overlaps the polygons. """
        from spira.yevon.utils import clipping
        pts = clipping.offset(points=self.outside.points)
        ply = Polygon(shape=pts[0], layer=self.outside.layer)
        if ply.intersection(other):
            return True
        return False

    def create_elementals(self, elems):
        elems += self.inside
        elems += self.outside
        return elems


class EdgeEuclidean(Edge):

    radius = NumberField(default=1)

    def __init__(self, **kwargs):
        pass

    def create_elementals(self, elems):

        return elems


class EdgeSquare(Edge):

    def __init__(self, **kwargs):
        pass

    def create_elementals(self, elems):

        return elems


class EdgeSideExtend(Edge):

    side_extend = NumberField(default=1)

    def __init__(self, **kwargs):
        pass

    def create_elementals(self, elems):

        return elems





import networkx as nx

from spira.core.typed_list import TypedList
from spira.core.parameters.descriptor import DataFieldDescriptor
from spira.core.parameters.restrictions import RestrictType


class EdgeList(TypedList):
    """ List containing nets for each metal plane in a cell. """

    __item_type__ = __Edge__

    def __repr__(self):
        if len(self._list) == 0: print('Edgelist is empty')
        return '\n'.join('{}'.format(k) for k in enumerate(self._list))

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._list[key]
        else:
            return self.get_from_label(key)

    def __delitem__(self, key):
        for i in range(0, len(self._list)):
            if self._list[i] is key:
                return list.__delitem__(self._list, i)

    def flat_copy(self, level = -1):
        el = EdgeList()
        for e in self._list:
            el += e.flat_copy(level)
        return el

    def move(self, position):
        for c in self._list:
            c.move(position)
        return self

    def move_copy(self, position):
        T = self.__class__()
        for c in self._list:
            T.append(c.move_copy(position))
        return T

    def transform_copy(self, transformation):
        T = self.__class__()
        for c in self._list:
            T.append(c.transform_copy(transformation))
        return T

    def transform(self, transformation):
        for c in self._list:
            c.transform(transformation)
        return self


class EdgeListField(DataFieldDescriptor):

    __type__ = EdgeList

    def __init__(self, default=[], **kwargs):
        kwargs['default'] = self.__type__(default)
        kwargs['restrictions'] = RestrictType([self.__type__])
        super().__init__(**kwargs)

    def __repr__(self):
        return ''

    def __str__(self):
        return ''

    def call_param_function(self, obj):
        f = self.get_param_function(obj)
        value = f(self.__type__())
        if value is None:
            value = self.__type__()
        new_value = self.__cache_parameter_value__(obj, value)
        return new_value



