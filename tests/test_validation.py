import cadquery as cq

from mechcad.validation import assert_valid, bounding_box


def test_bounding_box_and_validity() -> None:
    shape = cq.Workplane("XY").box(10, 20, 30)
    assert_valid(shape)
    assert bounding_box(shape).x == 10.0
    assert bounding_box(shape).y == 20.0
    assert bounding_box(shape).z == 30.0
