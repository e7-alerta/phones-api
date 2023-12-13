import dash.places.api as places_api
import dash.phones.api as phones_api


def find_place_by_phone_id(phone_id: str) -> places_api.Place:
    # print("[ place_manager ] find place by phone id :", phone_id)
    phone = phones_api.get_phone_by_id(phone_id)
    # print("[ place_manager ] phone :", phone)
    place = places_api.get_place_by_id(phone.place.id)
    return place
