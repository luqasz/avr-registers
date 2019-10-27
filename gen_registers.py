# -*- coding: UTF-8 -*-

from pathlib import Path
import yaml

from parser import parseString


def parse():
    for dev_file in Path('./atdf').glob('*.atdf'):
        yield from parseString(str(dev_file.resolve()))


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
    for device in set(parse()):
        yml = dict()
        yml['name'] = device['name'].lower()
        yml['registers'] = list(register(reg) for reg in device.registers)
        yield yml


if __name__ == '__main__':
    for device in generate():
        dst = Path('./registers') / (device['name'].lower() + '.yml')
        dst.touch()
        with dst.open('wt') as dst:
            yaml.dump(device, dst)
