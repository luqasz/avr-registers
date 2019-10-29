# -*- coding: UTF-8 -*-

from pathlib import Path
import yaml

from parser import parseFile


def parse():
    for dev_file in Path('./atdf').glob('*.atdf'):
        yield from parseFile(str(dev_file.resolve()))


def bit_field(field):
    return dict(
        name = field['name'],
        bit = field['mask'],
        description = field['caption'],
    )


def register(reg):
    return dict(
        name = reg['name'],
        address = reg['offset'],
        bit_fields = list(bit_field(field) for field in reg.bit_fields),
        description = reg['caption'],
    )


def generate():
    for device in parse():
        yml = dict()
        yml['name'] = device['name'].lower()
        yml['registers'] = list(register(reg) for reg in device.registers)
        yield yml


def filterDevices(yml):
    # No datasheet available
    return yml['name'] not in (
        'atmega64hve2',
        'atmega8hva',
        'atmega16hva',
        'atmega16hvb',
        'atmega16hvbrevb',
        'atmega32hvb',
        'atmega32hvbrevb',
        'atmega64hve2',
    )


if __name__ == '__main__':
    for device in filter(filterDevices, generate()):
        dst = Path('./registers') / (device['name'].lower() + '.yml')
        dst.touch()
        with dst.open('wt') as dst:
            yaml.dump(device, dst)
