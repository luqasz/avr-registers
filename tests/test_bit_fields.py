import pytest


def isPowerOfTwo(number):
    return (number & (number - 1)) == 0


def test_power_of_two(device):
    for reg in device['registers']:
        for field in reg['bit_fields']:
            bit = field['bit']
            assert isPowerOfTwo(bit), f"bit {field['name']} in {reg['name']} is not a power of two"


def test_WGM_bits_in_TCCR1A(TCCR1A):
    _, reg = TCCR1A
    fields = tuple(field['name'] for field in reg['bit_fields'])
    assert 'WGM10' in fields
    assert 'WGM11' in fields


def test_WGM_bits_in_TCCR1B(TCCR1B):
    device, reg = TCCR1B
    if device == 'atmega406':
        pytest.skip('Device has no WGM bits')
    fields = tuple(field['name'] for field in reg['bit_fields'])
    # Only WGM13 in TCCR1B
    if device not in ('at90pwm161', 'at90pwm81'):
        assert 'WGM12' in fields
    assert 'WGM13' in fields


def test_WGM_bits_in_TCCR3A(TCCR3A):
    _, reg = TCCR3A
    fields = tuple(field['name'] for field in reg['bit_fields'])
    assert 'WGM30' in fields
    assert 'WGM31' in fields


def test_WGM_bits_in_TCCR3B(TCCR3B):
    _, reg = TCCR3B
    fields = tuple(field['name'] for field in reg['bit_fields'])
    assert 'WGM32' in fields
    assert 'WGM33' in fields


def test_WGM_bits_in_TCCR4A(TCCR4A):
    device, reg = TCCR4A
    if device in ('atmega32u4', 'atmega16u4'):
        pytest.skip('Device has not WGM bits')
    fields = tuple(field['name'] for field in reg['bit_fields'])
    assert 'WGM40' in fields
    assert 'WGM41' in fields


def test_WGM_bits_in_TCCR4B(TCCR4B):
    device, reg = TCCR4B
    if device in ('atmega32u4', 'atmega16u4'):
        pytest.skip('Device has not WGM bits')
    fields = tuple(field['name'] for field in reg['bit_fields'])
    assert 'WGM42' in fields
    assert 'WGM43' in fields


def test_WGM_bits_in_TCCR5A(TCCR5A):
    _, reg = TCCR5A
    fields = tuple(field['name'] for field in reg['bit_fields'])
    assert 'WGM50' in fields
    assert 'WGM51' in fields


def test_WGM_bits_in_TCCR5B(TCCR5B):
    _, reg = TCCR5B
    fields = tuple(field['name'] for field in reg['bit_fields'])
    assert 'WGM52' in fields
    assert 'WGM53' in fields

