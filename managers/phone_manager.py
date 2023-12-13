from dash.types import GeoPoint, Place, Phone
import dash.places.api as places_api
import dash.phones.api as phones_api


def trigger_alarm(phone_id: str, trigger_form: dict):
    print("[ phone_manager ] trigger alarm :", phone_id, trigger_form)
    phone = phones_api.get_phone_by_id(phone_id)
    print("[ phone_manager ] phone :", phone)
    # place = places_api.get_place_by_id(phone.place.id)
    # print("[ phone_manager ] place :", place)
    return True


def refresh_token(phone_id: str, token: str):
    print("[ phone_manager ] refresh token :", phone_id, token)
    phones_api.update_token(phone_id, token)
    return True


def add_new_phone(new_phone_form: dict):
    print("[ phone_manager ] a new phone :", new_phone_form)

    print("[ phone_manager ] geopoint :", new_phone_form.get("geopoint"))
    geo_point = GeoPoint(
        type="Point",
        coordinates=[
            new_phone_form.get("geopoint").get("coordinates")[0],
            new_phone_form.get("geopoint").get("coordinates")[1],
        ]
    )

    new_place = Place(
        id=None,
        **new_phone_form
    )
    new_place.geopoint = geo_point

    place_stored = places_api.add_new_place(new_place)

    new_phone = Phone(
        id=None,
        name=None,
        phone_number=None,
        geopoint=geo_point,
        place=place_stored
    )

    phone_stored = phones_api.add_new_phone(new_phone)

    return [phone_stored, place_stored]
