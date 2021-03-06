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
        key = key.strip()
        if key == 'caption':
            return self.elem.attrib.get(key, '').strip()

        attr = self.elem.attrib[key].strip()

        if attr.startswith('0x'):
            return int(attr, 16)
        elif attr.isnumeric():
            return int(attr)
        else:
            return attr


class BitField (Hashable, Base, Sortable):

    def __init__(self, mask, name, caption):
        self._hash_ = mask
        self._lt_ = mask
        self.name = name
        self.mask = mask
        self.caption = caption


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


def filterFuses(register):
    return register['name'] not in (
        'LOCKBIT',
        'EXTENDED',
        'HIGH',
        'LOW',
    )


def bitPositions(num):
    position = 0
    while (position < 8):
        if (num >> position) & 1:
            yield position
        position += 1


def isPowerOfTwo(number):
    return (number & (number - 1)) == 0


def splitBitField(field):
    for num, position in enumerate(bitPositions(field['mask'])):
        yield BitField(
            name=field['name'] + str(num),
            mask=(1 << position),
            caption=field['caption'],
        )

def createBitFields(fields):
    for field in fields:
        field = AttrCast(elem=field)
        if isPowerOfTwo(field['mask']):
            yield BitField(
                name=field['name'],
                mask=field['mask'],
                caption=field['caption'],
            )
        else:
            yield from splitBitField(field)


def dedupRegisters(root):
    """
    Same registers are placed within different modules.
    Yield each unique register with all its found bit fields.
    """
    registers = defaultdict(set)
    for elem in root.findall('./modules/module/register-group/register'):
        reg = Register(elem)
        registers[reg].update(elem.findall('bitfield'))
    for reg, fields in registers.items():
        reg.bit_fields = set(createBitFields(fields))
        yield reg


def parseFile(file_name):
    """Parse given atdf file and yield each device as a Device object."""
    root = ElementTree.parse(file_name).getroot()
    devices = root.find('./devices')
    regs = filter(filterFuses, dedupRegisters(root))
    for elem in devices:
        device = Device(elem=elem)
        device.registers = tuple(regs)
        yield device
