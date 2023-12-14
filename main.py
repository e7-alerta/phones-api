from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from managers import phone_manager
from managers import place_manager

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello phones v1.3"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api/v1/phones/{phone_id}/place")
async def say_hello(phone_id: str):
    print("get place :", phone_id)
    place = place_manager.find_place_by_phone_id(phone_id)
    raw_place = place.model_dump()
    raw_place["geopoint"] = {
        "type": raw_place["geopoint"]["type"],
        "coordinates": raw_place["geopoint"]["coordinates"]
    }
    return {
        "data": raw_place
    }


class AskPhoneNumberForm(BaseModel):
    phone_id: str
    token: str


@app.post("/api/v1/phones/hooks/ask_phone_number")
async def ask_phone_number_hook(form: dict):
    ask_form = AskPhoneNumberForm(phone_id=form["phone_id"], token=form["changes"]["push_token"])
    print("[ api/v1/phones/hooks/ask_phone_number ] ask phone number |", ask_form)
    phone_manager.ask_phone_number(ask_form.phone_id, ask_form.token)
    return ask_form.model_dump()


class RefreshTokenForm(BaseModel):
    token: str


@app.patch("/api/v1/phones/{phone_id}/token/refresh")
async def update_token(phone_id: str, refresh_form: RefreshTokenForm):
    print("[ /api/v1/phones/{phone_id}/token/refresh ] update token | ", phone_id, refresh_form)
    phone_manager.refresh_token(phone_id, refresh_form.token)
    return {
        "data": {
            "id": phone_id
        }
    }


class TriggerAlarmForm(BaseModel):
    # phone_id: Optional[str]
    id: Optional[str]
    geopoint: Optional[dict]
    alert_type: Optional[str]
    alerted: Optional[bool]
    status: Optional[str]


@app.post("/api/v1/phones/{phone_id}/alerts/trigger")
async def trigger_alarm(phone_id: str, trigger_form: TriggerAlarmForm):
    print("trigger alarm :", phone_id, trigger_form)
    phone_manager.trigger_alarm(phone_id, trigger_form)
    return {
        "data": {
            "id": phone_id
        }
    }


@app.post("/api/v1/phones/new")
async def new_phone(new_phone_form: dict):
    print("[ /api/v1/phones/new ] a new device | ", new_phone_form)

    if new_phone_form.get("country_code") == "US":
        return {
            "data": {
                "id": "122c418c-4f58-4922-9b8b-a524c055035b",
                "phone_id": "122c418c-4f58-4922-9b8b-a524c055035b",
            }
        }

    # si el street number es None, entonces pongo 0
    if new_phone_form.get("street_number") is None:
        new_phone_form["street_number"] = "0"
    # si el street number es tiene - entonces lo separo y me quedo con el primero
    if "-" in new_phone_form.get("street_number"):
        new_phone_form["street_number"] = new_phone_form.get("street_number").split("-")[0]
    # si el street number es tiene caracteres no numericos, entonces los elimino
    if not new_phone_form.get("street_number").isnumeric():
        new_phone_form["street_number"] = "".join(
            [char for char in new_phone_form.get("street_number") if char.isnumeric()])

    if new_phone_form.get("street") is None:
        new_phone_form["street"] = ""

    if new_phone_form.get("city") is None:
        new_phone_form["city"] = ""

    if new_phone_form.get("subregion") is None:
        new_phone_form["subregion"] = ""

    [phone, place] = phone_manager.add_new_phone(new_phone_form)

    return {
        "data": {
            "id": phone.id,
            "phone_id": phone.id,
        }
    }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8070)
