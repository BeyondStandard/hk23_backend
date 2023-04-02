from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from geojson import Point, Polygon, LineString


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectId")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class PydanticMongoBase(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

class POI(PydanticMongoBase):
    name: str
    category_1: str
    category_2: str
    location: Point
    poly_5: Optional[Polygon]
    poly_10: Optional[Polygon]
    poly_15: Optional[Polygon]
    poly_20: Optional[Polygon]

class BikeRoute(PydanticMongoBase):
    year: int
    vehicle_type: str
    start: Point
    end: Point
    length: float
    valid: bool
    location: Optional[LineString]

class District(PydanticMongoBase):
    name: str
    location: Point
    poly: Polygon


if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient("mongodb+srv://fetch:ZydcdimtEoYVat51@maincluster.fc2z1.mongodb.net/")
    database = client["data"]

    result = database.poi.find_one({"_id": ObjectId("6428775b6f6fcc64dba32746")})
