# -*- coding: UTF-8 -*-

from zipfile import ZipFile
from xml.etree import ElementTree
from collections import defaultdict


class Base:

    def __str__(self):
        return str(self['name'])

    def __repr__(self):
        return f"<{self.__class__.__name__} {self['name']}>"


class Hashable:

    def __hash__(self):
        return hash(self._hash_)

    def __eq__(self, other):
        return hash(self) == hash(other)


class Sortable:

    def __lt__(self, other):
        return self._lt_ < other._lt_


class AttrCast:

    def __init__(self, elem):
        self.elem = elem

    def __getitem__(self, key):
        """Due to inconsistency in atdf files, some attributes are in hex and some as int."""
        attr = self.elem.attrib.get(key, '').strip()
        if attr.startswith('0x'):
            return int(attr, 16)
        elif attr.isnumeric():
            return int(attr)
        else:
            return attr


class BitField (Hashable, Base, Sortable, AttrCast):

    def __init__(self, elem):
        super().__init__(elem=elem)
        self._hash_ = self['name']
        self._lt_ = self['mask']


class Register(Hashable, Sortable, Base, AttrCast):

    def __init__(self, elem):
        super().__init__(elem=elem)
        self._hash_ = self['name']
        self._lt_ = self['offset']


class Interrupt(Hashable, Base, Sortable, AttrCast):

    def __init__(self, elem):
        super().__init__(elem=elem)
        self._hash_ = (self['name'])
        self._lt_ = self['index']


class MemorySegment(Hashable, Base, Sortable, AttrCast):

    def __init__(self, elem):
        super().__init__(elem=elem)
        self._hash_ = (self['name'])
        self._lt_ = self['name']


class AddressSpace(Hashable, Base, Sortable, AttrCast):

    def __init__(self, elem):
        super().__init__(elem=elem)
        self._hash_ = (self['name'])
        self._lt_ = self['name']

    @property
    def memory_segments(self):
        for elem in self.elem.findall('memory-segment'):
            yield MemorySegment(elem=elem)


class Device(Hashable, Base, AttrCast):

    def __init__(self, elem):
        super().__init__(elem=elem)
        self._hash_ = self['name']
        self._lt_ = self['name']

    @property
    def interrupts(self):
        for elem in self.elem.find('interrupts'):
            yield Interrupt(elem=elem)

    @property
    def address_spaces(self):
        for elem in self.elem.find('address-spaces'):
            yield AddressSpace(elem=elem)


def bitPositions(num):
    position = 0
    while (position < 8):
        if (num >> position) & 1:
            yield position
        position += 1


def isPowerOfTwo(number):
    return (number & (number - 1)) == 0


def dedupRegisters(root):
    """
    Same registers are placed within different modules.
    Yield each unique register with all its found bit fields.
    """
    registers = defaultdict(set)
    for elem in root.findall('./modules/module/register-group/register'):
        fields = (BitField(elem=e) for e in elem.findall('bitfield'))
        reg = Register(elem)
        registers[reg].update(fields)
    for reg, fields in registers.items():
        reg.bit_fields = fields
        yield reg


def parseString(file_name):
    """Parse given atdf file and yield each device as a Device object."""
    root = ElementTree.parse(file_name).getroot()
    devices = root.find('./devices')
    regs = tuple(dedupRegisters(root))
    for elem in devices:
        device = Device(elem=elem)
        device.registers = regs
        yield device
