from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, ObjectIdField
from geojson import Point, Polygon


class PydanticMongoBase(BaseModel):
    id: ObjectIdField = None

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

class POI(PydanticMongoBase):
    name: str
    category_1: str
    category_2: str
    location: Point
    poly_5: Polygon
    poly_10: Polygon
    poly_15: Polygon
    poly_20: Polygon

class POIRepository(AbstractRepository[POI]):
    class Meta:
        collection_name = "poi"

if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient("mongodb+srv://fetch:ZydcdimtEoYVat51@maincluster.fc2z1.mongodb.net/")
    database = client["data"]

    poi_repository = POIRepository(database=database)

    result = poi_repository.find_one_by_id(ObjectId("6428775b6f6fcc64dba32746"))
