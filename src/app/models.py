from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from geojson import Point, Polygon


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
    poly_5: Polygon
    poly_10: Polygon
    poly_15: Polygon
    poly_20: Polygon


if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient("mongodb+srv://fetch:ZydcdimtEoYVat51@maincluster.fc2z1.mongodb.net/")
    database = client["data"]

    poi_repository = database.poi

    result = poi_repository.find_one({"_id": ObjectId("6428775b6f6fcc64dba32746")})
