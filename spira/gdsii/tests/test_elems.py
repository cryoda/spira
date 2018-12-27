import spira
import pytest
from spira import param
from spira import shapes

UM = 1e6

# -------------------------------------------- spira.Polygon ----------------------------------------

def test_elem_polygon():
    p1 = [[[0,0], [3,0], [3,1], [0,1]]]
    p2 = [[[4,0], [7,0], [7,1], [4,1]]]
    p3 = [[[8,0], [11,0], [11,1], [8,1]]]

    # Create polygon using class parameters.
    ply1 = spira.Polygons(p1)
    assert issubclass(type(ply1.shape), shapes.Shape)
    assert ply1.gdslayer.number == 0
    assert ply1.gdslayer.datatype == 0

    # Create polygon using new layer number.
    ply2 = spira.Polygons(
        shape=p2,
        gdslayer=spira.Layer(number=77)
    )
    assert issubclass(type(ply2.shape), shapes.Shape)
    assert ply2.gdslayer.number == 77
    assert ply2.gdslayer.datatype == 0

    # Create polygon using new shape, number and datatype.
    ply3 = spira.Polygons(
        shape=shapes.Shape(points=p3),
        gdslayer=spira.Layer(number=51, datatype=1)
    )
    assert issubclass(type(ply3.shape), shapes.Shape)
    assert ply3.gdslayer.number == 51
    assert ply3.gdslayer.datatype == 1

# -------------------------------------------- spira.Label ------------------------------------------

def test_elem_label():
    l1 = spira.Label(position=(0,0), text='L1')
    assert all([a == b for a, b in zip(l1.position, [0,0])])
    assert l1.text == 'L1'
    assert l1.rotation == 0
    assert l1.magnification == 1
    assert l1.reflection == False
    assert l1.texttype == 0

# -------------------------------------------- spira.Cell -------------------------------------------

def test_elem_cell():
    c1 = spira.Cell(name='CellA')
    assert c1.name == 'CellA'
    assert len(c1.ports) == 0
    assert len(c1.elementals) == 0

    c1.ports += spira.Port(name='P1')
    assert len(c1.ports) == 1

    c1.elementals += spira.Polygons(shape=[[[0,0], [1,0], [1,1], [0,1]]])
    assert len(c1.elementals) == 1
    # assert c1.elementals[0].center == (0,0)

    # c1.move(destination=)

    class CellB(spira.Cell):

        def create_elementals(self, elems):

            elems += spira.Polygons(
                shape=[[[0,0], [3,0], [3,1], [0,1]]],
                gdslayer=spira.Layer(number=77)
            )

            return elems

    c2 = CellB()
    assert c2.name == 'CellB-0'
    assert len(c1.elementals) == 1
    assert isinstance(c2.elementals[0], spira.Polygons)

# -------------------------------------------- spira.SRef -------------------------------------------

def test_elem_sref():
    class CellB(spira.Cell):

        def create_elementals(self, elems):

            elems += spira.Polygons(
                shape=[[[0,0], [3,0], [3,1], [0,1]]],
                gdslayer=spira.Layer(number=77)
            )

            return elems

    c2 = CellB()

    s1 = spira.SRef(structure=c2)
    assert all([a == b for a, b in zip(s1.midpoint, [0,0])])
    assert s1.rotation == 0
    assert s1.magnification == 0
    assert s1.reflection == False

# -------------------------------------------- spira.Port -------------------------------------------

def test_elem_port():
    class PortExample(spira.Cell):

        def create_ports(self, ports):
            ports += spira.Port(name='P1', midpoint=(-1,2))
            ports += spira.Port(name='P2', midpoint=(0,3))
            return ports

    cell = PortExample()

    p1 = cell.ports[0]
    p2 = cell.ports[1]

    assert repr(p1) == '[SPiRA: Port] (name P1, midpoint (-1, 2))'

    assert p1.midpoint == [-1,2]
    assert p1.orientation == 0
    p1.reflect()
    assert p1.midpoint == [-1,-2]
    assert p1.orientation == 0
    p1.rotate(angle=90)
    assert p1.midpoint == [2,-1]
    assert p1.orientation == 90
    p1.translate(dx=10, dy=5)
    assert p1.midpoint == [12, 4]


# -------------------------------------------- spira.Term -------------------------------------------

def test_elem_terminal():
    class TerminalExample(spira.Cell):

        width = param.FloatField(default=10)
        height = param.FloatField(default=1)

        def create_ports(self, ports):
            ports += spira.Term(name='P1', midpoint=(10,0), width=self.height, orientation=180)
            return ports

    cell = TerminalExample()

    terms = cell.term_ports
    assert isinstance(terms['P1'], spira.Term)
    assert isinstance(cell.ports[0], spira.Term)
    assert isinstance(cell.terms[0], spira.Term)
    


