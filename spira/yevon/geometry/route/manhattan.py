import spira.all as spira
import numpy as np
from spira.core import param
from spira.yevon.gdsii.cell import Cell

from spira.yevon.geometry.route.route_shaper import RouteSimple
from spira.yevon.geometry.route.route_shaper import RouteGeneral
from spira.yevon.geometry.route.route_shaper import RouteArcShape
from spira.yevon.geometry.route.route_shaper import RouteSquareShape
from spira.yevon.rdd import get_rule_deck

from spira.yevon.geometry.ports.base import PortField
from spira.core.param.variables import *
from spira.yevon.layer import LayerField
from spira.yevon.rdd.layer import PhysicalLayerField
from spira.core.descriptor import DataField, FunctionField


RDD = get_rule_deck()


class __Manhattan__(Cell):

    port1 = PortField(default=None)
    port2 = PortField(default=None)

    length = NumberField(default=20*1e6)
    gds_layer = LayerField(number=13)
    ps_layer = PhysicalLayerField(default=RDD.DEF.PDEFAULT)
    # bend_type = StringField(default='rectangle')
    bend_type = StringField(default='circular')

    b1 = DataField(fdef_name='create_arc_bend_1')
    b2 = DataField(fdef_name='create_arc_bend_2')

    p1 = DataField(fdef_name='create_port1_position')
    p2 = DataField(fdef_name='create_port2_position')

    quadrant_one = DataField(fdef_name='create_quadrant_one')
    quadrant_two = DataField(fdef_name='create_quadrant_two')
    quadrant_three = DataField(fdef_name='create_quadrant_three')
    quadrant_four = DataField(fdef_name='create_quadrant_four')

    def get_radius(self):
        if self.port1 and self.port2:
            if hasattr(self, '__radius__'):
                return self.__radius__
            else:
                dx = abs(self.p2[0] - self.p1[0])
                dy = abs(self.p2[1] - self.p1[1])
                if dx <= dy:
                    self.__radius__ = dx*0.2
                elif dy <= dx:
                    self.__radius__ = dy*0.2
                # if dx <= dy:
                #     self.__radius__ = dx
                # elif dy <= dx:
                #     self.__radius__ = dy
                return self.__radius__

    def set_radius(self, value):
        self.__radius__ = value
    
    radius = FunctionField(get_radius, set_radius)

    def route_straight(self, p1, p2):
        route_shape = RouteSimple(
            port1=p1, port2=p2,
            path_type='straight',
            width_type='straight'
        )
        # route_shape.apply_merge
        R1 = RouteGeneral(route_shape=route_shape, connect_layer=self.ps_layer)
        r1 = spira.SRef(R1)
        # r1.rotate(angle=p2.orientation+90, center=R1.port_input.midpoint)
        r1._rotate(rotation=p2.orientation-90, center=R1.port_input.midpoint)
        r1.move(midpoint=(0,0), destination=p1.midpoint)
        return r1

    def create_port1_position(self):
        angle = np.mod(self.port1.orientation, 360)
        p1 = [self.port1.midpoint[0], self.port1.midpoint[1]]
        if angle == 90:
            p1 = [self.port1.midpoint[1], -self.port1.midpoint[0]]
        if angle == 180:
            p1 = [-self.port1.midpoint[0], -self.port1.midpoint[1]]
        if angle == 270:
            p1 = [-self.port1.midpoint[1], self.port1.midpoint[0]]
        return p1

    def create_port2_position(self):
        angle = np.mod(self.port1.orientation, 360)
        p2 = [self.port2.midpoint[0], self.port2.midpoint[1]]
        if angle == 90:
            p2 = [self.port2.midpoint[1], -self.port2.midpoint[0]]
        if angle == 180:
            p2 = [-self.port2.midpoint[0], -self.port2.midpoint[1]]
        if angle == 270:
            p2 = [-self.port2.midpoint[1], self.port2.midpoint[0]]
        return p2

    def create_arc_bend_1(self):
        if self.bend_type == 'circular':
            rs = RouteArcShape(
                radius=self.radius,
                width=self.port1.width,
                # gds_layer=self.gds_layer,
                # gds_layer=self.ps_layer.layer,
                start_angle=0, theta=90
            )
        if self.bend_type == 'rectangle':
            rs = RouteSquareShape(
                width=self.port1.width,
                size=(self.radius, self.radius)
            )
        B1 = RouteGeneral(route_shape=rs, connect_layer=self.ps_layer)
        return spira.SRef(B1)

    def create_arc_bend_2(self):
        if self.bend_type == 'circular':
            rs = RouteArcShape(
                radius=self.radius,
                width=self.port1.width,
                # gds_layer=self.gds_layer,
                # gds_layer=self.ps_layer.layer,
                start_angle=0, theta=-90
            )
        if self.bend_type == 'rectangle':
            rs = RouteSquareShape(
                width=self.port1.width,
                size=(self.radius, self.radius)
            )
        B1 = RouteGeneral(
            p1_name='Port1',
            p2_name='Port2',
            route_shape=rs, 
            connect_layer=self.ps_layer
        )
        return spira.SRef(B1)

    # def create_arc_bend_1(self):
    #     if self.bend_type == 'circular':
    #         B1 = Arc(shape=ArcRoute(
    #             radius=self.radius,
    #             width=self.port1.width,
    #             gds_layer=self.gds_layer,
    #             start_angle=0, theta=90)
    #         )
    #     if self.bend_type == 'rectangle':
    #         B1 = Rect(shape=RectRoute(
    #                 width=self.port1.width,
    #                 gds_layer=self.gds_layer,
    #                 # ps_layer=self.ps_layer,
    #                 size=(self.radius,self.radius)
    #             ),
    #             ps_layer=self.ps_layer
    #         )
    #     return spira.SRef(B1)

    # def create_arc_bend_2(self):
    #     if self.bend_type == 'circular':
    #         B2 = Arc(shape=ArcRoute(
    #             radius=self.radius,
    #             width=self.port1.width,
    #             gds_layer=self.gds_layer,
    #             start_angle=0, theta=-90)
    #         )
    #     if self.bend_type == 'rectangle':
    #         B2 = Rect(shape=RectRouteTwo(
    #                 width=self.port1.width,
    #                 gds_layer=self.gds_layer,
    #                 # ps_layer=self.ps_layer,
    #                 size=(self.radius,self.radius)
    #             ),
    #             ps_layer=self.ps_layer
    #         )
    #     return spira.SRef(B2)










