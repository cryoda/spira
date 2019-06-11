from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.geometry.ports.port_list import PortList


__all__ = ['ProcessBooleanFilter']


class ProcessBooleanFilter(Filter):
    
    def __filter___Cell____(self, item):
        ports = PortList()
        elems = ElementalList()
        for pg in item.process_elementals:
            for e in pg.elementals:
                elems += e
        for e in item.elementals.sref:
            elems += e
        for e in item.elementals.labels:
            elems += e
        for p in item.ports:
            ports += p
        return item.__class__(elementals=elems, ports=ports)

    def __repr__(self):
        return "[SPiRA: ProcessBooleanFilter] ()"


