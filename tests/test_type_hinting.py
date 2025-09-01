# THIS IS JUST A MANUAL PERSONAL TEST FOR TYPE HINTING

import pytest
from pytest import CaptureFixture

from qnty.variables import Area, Length, Pressure


def test_area_type_hinting(capsys: CaptureFixture[str]):
    a = Area("Area")
    a.set(5).square_meters

    l = Length("Length")
    l.set(10).picas

    p = Pressure("Pressure")
    p.set(15).gigapascals

    with capsys.disabled():
        print(a)
        print(l)
        print(p)
