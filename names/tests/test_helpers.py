import pytest

from names.helpers import most_common_prefix


@pytest.mark.parametrize("list1,list2,result", [
    (["car", "skoda", "fabia"], ["car", "skoda", "octavia"], "car_skoda"),
    ([], [], ""),
    (["car", "skoda"], [], ""),
    (["car"], ["car"], "car"),
    (["car"], ["car", "skoda"], "car"),
    (["car", "skoda", "fabia", "1.4"], ["car", "skoda", "octavia", "1.4"], "car_skoda"),
    (["car", "skoda"], ["car", "alfa", "romeo"], "car"),
    (["car"], ["bike"], "")
])
def test_most_common_prefix(list1, list2, result):
    assert most_common_prefix(list1, list2, "_") == result
