# THIS IS JUST A MANUAL PERSONAL TEST FOR TYPE HINTING

from pytest import CaptureFixture

from qnty.quantities._field_qnty_generated import Area, Length, Pressure


def test_area_type_hinting(capsys: CaptureFixture[str]):
    a = Area("Area")
    a.set(5).square_meter

    length = Length("Length")
    length.set(10).pica

    p = Pressure("Pressure")
    p.set(15).gigapascal

    with capsys.disabled():
        print(a)
        print(length)
        print(p)
