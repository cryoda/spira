import sys

import spira.log as LOG

from spira.rdd import get_rule_deck
RDD = get_rule_deck()

from spira.kernel.io import import_gds

from spira.kernel.library import Library

from spira.kernel.cell import Cell
from spira.kernel.layer import Layer

from spira.kernel.elemental.port import Port
from spira.kernel.elemental.sref import SRef
from spira.kernel.elemental.aref import ARef
from spira.kernel.elemental.path import Path
from spira.kernel.elemental.label import Label
from spira.kernel.elemental.polygons import Polygons

from spira.lne.mesh import Mesh
from spira.lne.graph import Graph
from spira.lne.geometry import Geometry

from spira.lgm.shape.basic import Box
from spira.lgm.shape.basic import Rectangle
from spira.lgm.shape.basic import Circle

from spira.kernel.parameters.field.element_list import ElementList
from spira.kernel.primitive import *
from spira.kernel import param

def initialize():
    from spira import log as LOG
    from . import settings
    spira.LOG.start(name=settings.LIB_NAME, text=settings.START_MESSAGE)

initialize()
