from typing import Optional

from dash.types import GeoPoint, Place, Phone
import dash.places.api as places_api
import dash.phones.api as phones_api
from pusher import pusher_client
from pydantic import BaseModel
from pusher.client import PushForm


class TriggerAlarmForm(BaseModel):
    # phone_id: Optional[str]
    id: Optional[str] = None
    geopoint: Optional[dict] = None
    alert_type: Optional[str] = None
    alerted: Optional[bool] = None
    status: Optional[str] = None


def trigger_alarm(phone_id: str, trigger_form: TriggerAlarmForm = None):
    print("[ phone_manager ] trigger alarm :", phone_id, trigger_form)
    phone = phones_api.get_phone_by_id(phone_id)
    print("[ phone_manager ] phone :", phone)
    # place = places_api.get_place_by_id(phone.place.id)
    # print("[ phone_manager ] place :", place)
    phones_api.alert_phone(phone_id=phone_id, alert_type=trigger_form.alert_type)
    return True


def refresh_token(phone_id: str, token: str):
    # print("[ phone_manager ] refresh token :", phone_id, token)
    phones_api.update_token(phone_id, token)
    return True


def add_new_phone(new_phone_form: dict):
    # print("[ phone_manager ] a new phone :", new_phone_form)

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


def ask_phone_number(phone_id, token):
    # send a push notification to the phone
    # invite to talk by whatsapp
    form = PushForm(
        token=token,
        title="Bienvenido Vecino!",
        message="Felicitaciones, charlemos por whatsapp para presentarnos.",
        data={
            'message_type': 'greeting_talk',
            'has_phone': False,
            'contact_number': '5491128835917'
        }
    )

    pusher_client.push(form)
    return None
