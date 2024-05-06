from typing import Union
from fastapi import Depends, FastAPI, HTTPException
from mangum import Mangum
from sqlalchemy.orm import Session

import crud, models, schemas
from api.station import *
from api.bus import *
from api.route import *
from database import SessionLocal, engine
import json

from dotenv import load_dotenv
import os

# json file 경로
file_path = "api/busColor.json"
with open(file_path, encoding="UTF-8") as json_file:
    busColorData = json.load(json_file)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

#models.Base.metadata.create_all(bind=engine)
openApiEndpoint = "http://apis.data.go.kr/1613000"


app = FastAPI()
handler = Mangum(app)

# 의존성 주입
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"Hello":"FastAPI!"}

@app.get("/api/v1/station")
async def read_station_by_location(lat: float, lon: float, skip: int = 0):
    url = f"{openApiEndpoint}/BusSttnInfoInqireService/getCrdntPrxmtSttnList?serviceKey={os.environ["data_go_kr_key"]}&_type=json&gpsLati={lat}&gpsLong={lon}"
    return await get_station(url, skip)

@app.get("/api/v1/bus")
async def read_buses_by_station(stationId: str, cityCode: int):
    url = f"{openApiEndpoint}/BusSttnInfoInqireService/getSttnThrghRouteList?serviceKey={os.environ["data_go_kr_key"]}&_type=json&cityCode={cityCode}&nodeid={stationId}"
    data = await get_curSttnBusList(url, busColorData)
    url = f"{openApiEndpoint}/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList?serviceKey={os.environ["data_go_kr_key"]}&_type=json&cityCode={cityCode}&nodeId={stationId}"
    return await get_arvlBusList(url, data)

@app.get("/api/v1/route")
async def read_route_details(busId: str, cityCode: int):
    cityCodeUrl = f"{openApiEndpoint}/BusRouteInfoInqireService/getCtyCodeList?serviceKey={os.environ["data_go_kr_key"]}&_type=json"
    url = f"{openApiEndpoint}/BusRouteInfoInqireService/getRouteInfoIem?serviceKey={os.environ["data_go_kr_key"]}&_type=json&cityCode={cityCode}&routeId={busId}"
    return await get_route(url, cityCodeUrl, cityCode, busColorData)