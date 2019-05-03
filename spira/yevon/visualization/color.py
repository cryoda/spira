import spira.all as spira
# from spira.core import param
from spira.core.param.variables import StringField, IntegerField
from spira.core.initializer import FieldInitializer
from spira.core.descriptor import DataFieldDescriptor
from spira.core.param.restrictions import RestrictType


# Color Map: https://www.rapidtables.com/web/color/html-color-codes.html


class Color(FieldInitializer):
    """ Defines a color in terms of a name and RGB values. """

    # name = param.StringField(default='black')
    # red = param.IntegerField(default=0)
    # green = param.IntegerField(default=0)
    # blue = param.IntegerField(default=0)
    
    name = StringField(default='black')
    red = IntegerField(default=0)
    green = IntegerField(default=0)
    blue = IntegerField(default=0)

    def __init__(self, red=0, green=0, blue=0, **kwargs):
        super().__init__(red=red, green=green, blue=blue, **kwargs)

    def rgb_tuple(self):
        return (self.red, self.green, self.blue)

    def numpy_array(self):
        import numpy
        return numpy.array([self.red, self.green, self.blue])

    def set(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    @property
    def hexcode(self):
        return '#{:02x}{:02x}{:02x}'.format(int(self.red), int(self.green), int(self.blue))

    def __eq__(self, other):
        return other.red == self.red and other.green == self.green and other.blue == self.blue

    def __neq__(self, other):
        return other.red != self.red or other.green != self.green or other.blue != self.blue

    def __repr__(self):
        return ("[SPiRA: Color] (name '{}', hex {})").format(self.name, self.hexcode)

    def __str__(self):
        return self.__repr__()


COLOR_BLACK = Color(name='black', red=0, green=0, blue=0)
COLOR_WHITE = Color(name='white', red=255, green=255, blue=255)
COLOR_GREEN = Color(name='green', red=0, green=128, blue=0)
COLOR_LIGHT_GREEN = Color(name='light green', red=144, green=238, blue=144)
COLOR_BLUE = Color(name='blue', red=0, green=0, blue=255)
COLOR_CYAN = Color(name='cyan', red=0, green=255, blue=255)
COLOR_YELLOW = Color(name='yellow', red=255, green=255, blue=0)
COLOR_SILVER = Color(name='silver', red=192, green=192, blue=192)
COLOR_GRAY = Color(name='gray', red=128, green=128, blue=128)
COLOR_LIGHT_GRAY = Color(name='light gray', red=211, green=211, blue=211)
COLOR_BLUE_VIOLET = Color(name='blue violet', red=238, green=130, blue=238)
COLOR_GHOSTWHITE = Color(name='ghost white', red=248, green=248, blue=255)
COLOR_SALMON = Color(name='salmon', red=250, green=128, blue=144)
COLOR_CADET_BLUE = Color(name='cadet blue', red=95, green=158, blue=160)
COLOR_TURQUOISE = Color(name='turquoise', red=95, green=158, blue=160)
COLOR_CORAL = Color(name='coral', red=255, green=127, blue=80)
COLOR_AZURE = Color(name='azure', red=240, green=255, blue=255)
COLOR_PLUM = Color(name='plum', red=221, green=160, blue=221)
COLOR_DARK_SLATE_GREY = Color(name='dark slate grey', red=47, green=79, blue=79)
COLOR_DARKSEA_GREEN = Color(name='darksea green', red=143, green=188, blue=143)
COLOR_INDIAN_RED = Color(name='indian red', red=205, green=92, blue=92)
COLOR_STEEL_BLUE = Color(name='steel blue', red=70, green=130, blue=180)
COLOR_DARK_MAGENTA = Color(name='dark magenta', red=139, green=0, blue=139)
COLOR_ROYAL_BLUE = Color(name='royal blue', red=65, green=105, blue=225)


def ColorField(red=0, green=0, blue=0, **kwargs):
    from spira.yevon.visualization.color import Color
    if 'default' not in kwargs:
        kwargs['default'] = Color(red=0, green=0, blue=0, **kwargs)
    R = RestrictType(Color)
    return DataFieldDescriptor(restrictions=R, **kwargs)



