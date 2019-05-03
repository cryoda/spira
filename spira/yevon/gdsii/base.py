import spira.all as spira
from spira.core import param
from spira.core.transformable import Transformable
from spira.core.initializer import FieldInitializer
from spira.core.initializer import MetaElemental
from spira.core.descriptor import FunctionField
from spira.core.elem_list import ElementalListField


class __Elemental__(Transformable, FieldInitializer, metaclass=MetaElemental):
    """ Base class for all transformable elementals. """

    def get_node_id(self):
        if self.__id__:
            return self.__id__
        else:
            return self.__str__()

    def set_node_id(self, value):
        self.__id__ = value

    node_id = FunctionField(get_node_id, set_node_id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def flatten(self):
        return [self]

    def commit_to_gdspy(self, cell, transformation=None):
        return None

    def dependencies(self):
        return None

    def __add__(self, other):
        if isinstance(other, list):
            l = spira.ElementList([self])
            l.extend(other)
            return l
        elif isinstance(other, __Elemental__):
            return spira.ElementList([self, other])
        else:
            raise TypeError("Wrong type of argument for addition in __Elemental__: " + str(type(other)))

    def __radd__(self, other):
        if isinstance(other, list):
            l = spira.ElementList(other)
            l.append(self)
            return l
        elif isinstance(other, __Elemental__):
            return spira.ElementList([other, self])
        else:
            raise TypeError("Wrong type of argument for addition in __Elemental__: " + str(type(other)))


class __Group__(FieldInitializer):

    elementals = ElementalListField(fdef_name='create_elementals', doc='List of elementals to be added to the cell instance.')

    def create_elementals(self, elems):
        result = spira.ElementList()
        return result

    # FIXME: For some reason this interferes with the spira.Cell commit.
    # def commit_to_gdspy(self, cell, transformation=None):
    #     for e in self.elementals:
    #         e.commit_to_gdspy(cell=cell, transformation=transformation)
    #     return cell

    def append(self, element):
        el = self.elementals
        el.append(element)
        self.elementals = el

    def extend(self, elems):
        from spira.yevon.gdsii.group import Group
        el = self.elementals
        if isinstance(elems, Group):
            el.extend(elems.elemetals)
        else:
            el.extend(elems)
        self.elementals = el  

    def __iadd__(self, element):
        from spira.yevon import process as pc
        from spira.yevon.geometry.ports.base import __Port__
        """ Add elemental and reduce the class to a simple compound elementals. """
        if isinstance(element, (list, spira.ElementList)):
            self.extend(element)
        elif isinstance(element, (__Elemental__, pc.ProcessLayer)):
            self.append(element)
        elif element is None:
            return self
        elif issubclass(type(element), __Port__):
            self.ports += other
        else:
            raise TypeError("Invalid type " + str(type(element)) + " in __Group__.__iadd__().")
        return self

    def add_el(self, elems):
        self.elementals += elems

    def flatten(self, level = -1):
        self.elementals = self.elementals.flat_copy(level=level)
        return self

    def __iter__(self):
        return self.elementals.__iter__()

    def is_empty(self):
        return self.elementals.is_empty()

    # def __eq__(self,other):
    #     if other == None:
    #         return False
    #     if not isinstance(other, spira.Cell):
    #         return False
    #     self_el = self.elementals
    #     other_el = other.elementals
    #     if len(self_el) != len(other_el):
    #         return False
    #     for e1, e2 in zip(self_el, other_el):
    #         if (e1 != e2):
    #             return False
    #     return True

    # def __ne__(self, other):
    #     return not self.__eq__(other)