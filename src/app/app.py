from typing import Any, Optional, Union
from bson import ObjectId
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from app.models import BikeRoute, POI

app = FastAPI(title="HK23 API")

mongo_client = MongoClient("mongodb+srv://fetch:ZydcdimtEoYVat51@maincluster.fc2z1.mongodb.net/")
database = mongo_client["data"]

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "*",
    "http://127.0.0.1:8089/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def read_main():
    return {"msg": "Hello World !!!!"}


@app.get("/points_of_interest")
async def get_points_of_interest(field: Optional[str] = None, value: Optional[Union[str, int]] = None, limit: int = 20, poly_5: bool = False, poly_10: bool = False, poly_15: bool = False, poly_20: bool = False):
    excludes = {"poly_5": 0, "poly_10": 0, "poly_15": 0, "poly_20": 0}
    if poly_5:
        del excludes["poly_5"]
    if poly_10:
        del excludes["poly_10"]
    if poly_15:
        del excludes["poly_15"]
    if poly_20:
        del excludes["poly_20"]

    if not field or not value:
        result = [POI(**x) for x in database.poi.find({}, excludes, limit=limit)]
    elif field in ["_id", "id"]:
        result = POI(**database.poi.find_one({"_id": ObjectId(str(value))}, excludes))
    else:
        result = [POI(**x) for x in database.poi.find({field: value}, excludes, limit=limit)]
    return { "result": result }

@app.get("/bike_routes")
async def get_bike_routes(field: Optional[str] = None, value: Optional[Union[str, int]] = None, limit: int = 20, location: bool = False):
    excludes = {"location": 0}
    if location:
        del excludes["location"]

    if not field or not value:        
        result = [BikeRoute(**x) for x in database.bike_routes.find({}, excludes, limit=limit)]
    elif field in ["_id", "id"]:
        result = BikeRoute(**database.bike_routes.find_one({"_id": ObjectId(str(value))}, excludes))
    else:
        result = [BikeRoute(**x) for x in database.bike_routes.find({field: value}, excludes, limit=limit)]
    return { "result": result }
