from core.utils import getIndex

def test_full_index():
    assert getIndex([3,5,6,6,9,15,15],9) == 5

def test_float_index():
    assert getIndex([3,5,6,6,9,15,15],9.1) == 5

def test_less_index():
    assert getIndex([3,5,6,6,9,15,15],8.9) == 4

def test_first_index():
    assert getIndex([3,5,6,6,9,15,15],2.9) == 0

def test_last_index():
    assert getIndex([3,5,6,6,9,15,15],16) == 7

def test_repeative_index():
    assert getIndex([3,5,6,6,9,15,15],5.9) == 2