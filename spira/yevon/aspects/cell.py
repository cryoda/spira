import gdspy
import numpy as np

from copy import deepcopy
from spira.yevon.gdsii.group import __Group__
from spira.yevon.aspects.geometry import __GeometryAspects__


class CellAspects(__Group__, __GeometryAspects__):

    @property
    def bbox(self):
        D = deepcopy(self)
        cell = D.get_gdspy_cell()
        bbox = cell.get_bounding_box()
        if bbox is None:
            bbox = ((0,0),(0,0))
        return np.array(bbox)






# from spira.yevon.gdsii.cell import Cell
# from spira.yevon.aspects.base import __Aspects__
# from spira.yevon.gdsii.elem_list import ElementalListField, ElementalList
# from spira.yevon.filters.layer_filter import LayerFilterAllow
# from spira.yevon.utils import clipping
# from spira.yevon.gdsii.polygon import Polygon
# from spira.yevon.process import get_rule_deck


# RDD = get_rule_deck()


# def union_process_polygons(elems, process):

#     el = ElementalList()

#     for layer in RDD.get_physical_layers_by_process(processes=process):
#         LF = LayerFilterAllow(layers=[layer])
#         points = []
#         for e in LF(elems.polygons):
#             points.append(e.points)
#         merged_points = clipping.union_points(points)
#         for uid, pts in enumerate(merged_points):
#             el += Polygon(shape=pts, layer=layer)
#         return el


# # def get_process_elementals(elems, process):

# #     el = ElementalList()

# #     for layer in RDD.get_physical_layers_by_process(processes=process):
# #         LF = LayerFilterAllow(layers=[layer])
# #         points = []
# #         for e in LF(elems.polygons):
# #             points.append(e.points)
# #         merged_points = clipping.union_points(points)
# #         for uid, pts in enumerate(merged_points):
# #             el += Polygon(shape=pts, layer=layer)
# #         return el


# class ElementalsForModelling(__Aspects__):
#     """
#     Convert the cell elementals into a new set
#     of elements for every active process.
#     """

#     process_elementals = ElementalListField()

#     def create_process_elementals(self, elems):
#         for process in RDD.VMODEL.PROCESS_FLOW.active_processes:
#             # for e in get_process_elementals(self.elementals, process=process):
#             for e in union_process_polygons(self.elementals, process=process):
#                 elems += e
#         return elems

#     def write_gdsii_mask(self, **kwargs):
#         D = Cell(name=self.name + '_VMODEL', elementals=self.process_elementals)
#         D.output()


# class ReferenceBlocks(__Aspects__):

#     block_elementals = ElementalListField()

#     def create_block_elementals(self, elems):

#         for e in self.elementals.sref:
#             for layer in RDD.get_physical_layers_by_purpose(purposes=['METAL', 'GND']):
#                 if e.ref.is_layer_in_cell(layer):
#                     bbox_shape = e.bbox_info.bounding_box()
#                     elems += Polygon(shape=bbox_shape, layer=layer)

#         return elems

#     def write_gdsii_blocks(self, **kwargs):
#         D = Cell(name=self.name + '_BLOCKS', elementals=self.block_elementals)
#         D.output()


# # Cell.mixin(ElementalsForModelling)
# # Cell.mixin(ReferenceBlocks)


# # You have the different virtual models of defining the polygons structures,
# # before generating a physical gmsh geomtery.
