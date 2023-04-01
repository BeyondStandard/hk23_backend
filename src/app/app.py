from typing import Any, Union
from bson import ObjectId
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from app.models import POI

app = FastAPI(title="HK23 API")

mongo_client = MongoClient("mongodb+srv://fetch:ZydcdimtEoYVat51@maincluster.fc2z1.mongodb.net/")
database = mongo_client["data"]
poi_repository = database.poi

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


@app.get("/points_of_interest/{field}/{value}")
async def get_point_of_interest(field: str, value: Union[str, int], limit: int = 5, poly_5: bool = False, poly_10: bool = False, poly_15: bool = False, poly_20: bool = False):
    excludes = {"poly_5": 0, "poly_10": 0, "poly_15": 0, "poly_20": 0}
    if poly_5:
        del excludes["poly_5"]
    if poly_10:
        del excludes["poly_10"]
    if poly_15:
        del excludes["poly_15"]
    if poly_20:
        del excludes["poly_20"]

    if field in ["_id", "id"]:
        result = POI(**poi_repository.find_one({"_id": ObjectId(str(value))}, excludes))
    else:
        result = [POI(**x) for x in poi_repository.find({field: value}, excludes, limit=limit)]
    return { "result": result }

# @app.get("/get_user_by_id")
# async def get_user(user_id: str):
#     data = read_json("people_v3.json")
#     user = list(filter(lambda p_id: p_id["id"] == user_id, data))[0]
#     return user


# @app.get("/get_stations")
# async def get_stations():
#     stations = read_json("stations_v2.json")
#     return stations


# @app.get("/get_charging_stations")
# async def get_charging_stations():
#     charging_stations = read_json("charging_stations.json")
#     return charging_stations


# @app.get("/get_all_users")
# async def get_all_users():
#     users = read_json("people_v3.json")
#     return users

