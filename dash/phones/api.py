import requests

from dash.types import Phone, Place

PHONE_URL = "https://dash.vecinos.com.ar/items/phones"
HEADERS = {
    "Content-Type": "application/json",
}


def get_phone_by_id(phone_id: str):
    print("[ phone_api ] get phone by id :", phone_id)
    response = requests.get(
        PHONE_URL + "/" + phone_id,
        headers=HEADERS
    )
    if not response.status_code == 200:
        print("[ phone_api ] error :", response.status_code, response.json())
        return None

    phone = Phone(
        id=response.json().get("data").get("id"),
        status=response.json().get("data").get("status"),
        name=response.json().get("data").get("name"),
        phone_number=response.json().get("data").get("phone_number"),
        geopoint=response.json().get("data").get("geopoint"),
        place=Place(
            id=response.json().get("data").get("place")
        )
    )
    return phone


def update_token(phone_id: str, token: str):
    print("[ phone_api ] refresh token :", phone_id, token)
    response = requests.patch(
        PHONE_URL + "/" + phone_id,
        headers=HEADERS,
        json={
            "push_token": token,
            "status": "online"
        }
    )
    if not response.status_code == 200:
        print("[ phone_api ] error :", response.status_code, response.json())
        return None
    return True


def add_new_phone(new_phone: Phone):
    print("[ phone_api ] a new phone :", new_phone)

    # make payload from new_phone avoid None values
    payload = {}
    for key, value in new_phone.dict().items():
        if key == "place" and value is not None:
            payload["place"] = value.get("id")
        if value is not None:
            payload[key] = value
    print("[ phone_api ] payload :", payload)

    response = requests.post(
        PHONE_URL,
        headers=HEADERS,
        json=payload
    )
    if response.status_code == 200:
        new_phone.id = response.json().get("data").get("id")
        return new_phone
    else:
        print("[ phone_api ] error :", response.status_code, response.json())
        return None
