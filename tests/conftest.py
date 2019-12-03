from pathlib import Path

import pytest
import yaml


def parsed():
    for yml in Path('./registers').glob('*.yml'):
        with yml.open('rt') as fobj:
            yield yml.name.rstrip('.yml'), yaml.load(fobj, Loader=yaml.FullLoader)


def device_reg(devices, needle):
    for device in devices:
        for reg in device['registers']:
            if needle(reg['name']):
                yield device['name'], reg


def id_device_reg(param):
    dev_name, reg = param
    return dev_name


all_devices = tuple(dict(name=name, registers=regs) for name, regs in parsed())


@pytest.fixture(
    ids=lambda x: x['name'],
    params=all_devices,
)
def device(request):
    yield request.param


@pytest.fixture(ids=id_device_reg, params=device_reg(
    devices=all_devices,
    needle=lambda x: x.startswith('OCDR'),
))
def OCDR(request):
    return request.param


@pytest.fixture(ids=id_device_reg, params=device_reg(
    devices=all_devices,
    needle=lambda x: x.startswith('GPIOR'),
))
def GPIOR(request):
    return request.param


@pytest.fixture(ids=id_device_reg, params=device_reg(
    devices=all_devices,
    needle=lambda x: x == 'TCCR1A',
))
def TCCR1A(request):
    return request.param


@pytest.fixture(ids=id_device_reg, params=device_reg(
    devices=all_devices,
    needle=lambda x: x == 'TCCR1B',
))
def TCCR1B(request):
    return request.param


@pytest.fixture(ids=id_device_reg, params=device_reg(
    devices=all_devices,
    needle=lambda x: x == 'TCCR3A',
))
def TCCR3A(request):
    return request.param


@pytest.fixture(ids=id_device_reg, params=device_reg(
    devices=all_devices,
    needle=lambda x: x == 'TCCR3B',
))
def TCCR3B(request):
    return request.param


@pytest.fixture(ids=id_device_reg, params=device_reg(
    devices=all_devices,
    needle=lambda x: x == 'TCCR4A',
))
def TCCR4A(request):
    return request.param


@pytest.fixture(ids=id_device_reg, params=device_reg(
    devices=all_devices,
    needle=lambda x: x == 'TCCR4B',
))
def TCCR4B(request):
    return request.param


@pytest.fixture(ids=id_device_reg, params=device_reg(
    devices=all_devices,
    needle=lambda x: x == 'TCCR5A',
))
def TCCR5A(request):
    return request.param


@pytest.fixture(ids=id_device_reg, params=device_reg(
    devices=all_devices,
    needle=lambda x: x == 'TCCR5B',
))
def TCCR5B(request):
    return request.param
