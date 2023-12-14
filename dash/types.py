from typing import Optional, Any

from pydantic import BaseModel


class GeoPoint(BaseModel):
    type: str
    coordinates: list


class Place(BaseModel):
    id: Optional[str] = None
    status: Optional[str] = None
    name: Optional[str] = None
    geopoint: Optional[GeoPoint] = None
    address: Optional[str] = None
    street: Optional[str] = None
    street_number: Optional[int] = None
    country_code: Optional[str] = None
    country: Optional[str] = None
    raw_city: Optional[str] = None
    raw_district: Optional[str] = None
    raw_region: Optional[str] = None
    raw_subregion: Optional[str] = None
    postal_code: Optional[str] = None
    raw_country: Optional[str] = None


class Phone(BaseModel):
    id: Optional[str]
    phone_number: Optional[str]
    name: Optional[str]
    geopoint: GeoPoint
    place: Optional[Place]
