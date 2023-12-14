import requests

from dash.types import Place, GeoPoint

PLACE_URL = "https://dash.vecinos.com.ar/items/places"
HEADERS = {
    "Content-Type": "application/json",
}


def get_place_by_id(place_id: str):
    print("[ place_api ] get place by id :", place_id)
    response = requests.get(
        PLACE_URL + "/" + place_id,
        headers=HEADERS
    )
    if not response.status_code == 200:
        print("[ place_api ] error :", response.status_code, response.json())
        return None
    raw_place = {}
    # only get the fields that not None
    for key, value in response.json().get("data").items():
        print(key, value)
        # avoid geopoint and phones and devices and contacts
        if key == "geopoint" or key == "phones" or key == "iot_devices" or key == "contacts":
            continue
        if value is not None:
            raw_place[key] = value

    # print("[ place_api ] raw_place :", raw_place)
    geopint = GeoPoint(
        type="Point",
        coordinates=[
            response.json().get("data").get("geopoint").get("coordinates")[0],
            response.json().get("data").get("geopoint").get("coordinates")[1]
        ]
    )
    place = Place(**raw_place, geopoint=geopint)
    return place


def add_new_place(new_place: Place):
    # print("[ place_api ] a new place :", new_place)

    # make payload from new_place avoid None values
    payload = {}
    for key, value in new_place.dict().items():
        if value is not None:
            payload[key] = value
    # print("[ place_api ] payload :", payload)
    response = requests.post(PLACE_URL, json=payload)
    if response.status_code == 200:
        new_place.id = response.json().get("data").get("id")
        return new_place
    else:
        print("[ place_api ] error :", response.status_code, response.json())
        return None
