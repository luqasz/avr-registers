import pytest


def test_OCDR(OCDR):
    """OCDR is a data register without bit fields."""
    _, reg = OCDR
    assert reg['bit_fields'] == []


def test_GPIOR(GPIOR):
    """GPIOR is a data register without bit fields."""
    _, reg = GPIOR
    assert reg['bit_fields'] == []
