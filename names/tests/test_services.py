import pytest

from names.services import group_names


@pytest.mark.parametrize("names,result",[
    (["car_skoda", "car_volkswagen", "bike_suzuki"], {"bike_suzuki": ["bike_suzuki"], "car": ["car_skoda", "car_volkswagen"]}),
    ([], {}),
    (["car_skoda"], {"car_skoda": ["car_skoda"]}),
    (["car_skoda", "car_seat", "car_alfa_romeo", "car_land_rover"], {"car": ["car_alfa_romeo", "car_land_rover", "car_seat", "car_skoda"]}),
    (["car_skoda_fabia", "car_skoda_octavia", "car_seat_ibiza", "car_seat_leon"], {"car_seat": ["car_seat_ibiza", "car_seat_leon"], "car_skoda": ["car_skoda_fabia", "car_skoda_octavia"]}),
    (["car_skoda_fabia_1.9", "car_skoda_fabia_1.4"], {"car_skoda_fabia": ["car_skoda_fabia_1.4", "car_skoda_fabia_1.9"]}),
    (["car_bmw", "bike_bmw"], {"bike_bmw": ["bike_bmw"], "car_bmw": ["car_bmw"]}),
    (["car_renault_5", "car_bmw_5"], {"car": ["car_bmw_5", "car_renault_5"]}),
    (["car_skoda_fabia", "car_skoda_octavia", "car_skoda_fabia"], {"car_skoda": ["car_skoda_fabia", "car_skoda_octavia"]}),
    (["car_skoda_fabia", "car_skoda_octavia", "car_skoda_suberb", "car_skoda_roomster"], {"car_skoda": ["car_skoda_fabia", "car_skoda_octavia", "car_skoda_roomster", "car_skoda_suberb"]}),
    (["car_skoda", "car_skoda", "car_skoda"], {"car_skoda": ["car_skoda"]}),
    (["car", "car_skoda", "car_skoda_fabia"], {"car": ["car"], "car_skoda": ["car_skoda", "car_skoda_fabia"]})
])
def test_group_names(names, result):
    print(group_names(names))
    assert group_names(names) == result
