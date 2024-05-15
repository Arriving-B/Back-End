from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from sqlalchemy.orm import Session

import models, schemas
from api.station import *
from api.bus import *
from api.route import *
from api.feedback import *
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

models.Base.metadata.create_all(bind=engine)    
openApiEndpoint = "http://apis.data.go.kr/1613000"


app = FastAPI()
handler = Mangum(app)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)

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

@app.get("/api/v1/route/map")
async def read_route_details(busId: str, cityCode: int):
    url = f"{openApiEndpoint}/BusRouteInfoInqireService/getRouteAcctoThrghSttnList?serviceKey={os.environ["data_go_kr_key"]}&pageNo=1&numOfRows=200&_type=json&cityCode={cityCode}&routeId={busId}"
    return await get_routeMap(url)

@app.get("/api/v1/search")
async def read_search(cityCode: int, context: str):
    # 준비반
    busFindUrl = f"{openApiEndpoint}/BusRouteInfoInqireService/getRouteNoList?serviceKey={os.environ["data_go_kr_key"]}&pageNo=1&numOfRows=100&_type=json&cityCode={cityCode}&routeNo={context}"
    stationFindUrl = f"{openApiEndpoint}/BusSttnInfoInqireService/getSttnNoList?serviceKey={os.environ["data_go_kr_key"]}&pageNo=1&numOfRows=100&_type=json&cityCode={cityCode}&nodeNm={context}"
    
    try: 
        # 연산반
        busList = await get_busByContext(busFindUrl, busColorData)
        stationList = await get_stationByContext(stationFindUrl)

        # 응답반
        status = 200 if busList or stationList else 204
        return {
            "status": status,
            "message": "Search successful" if status == 200 else "No content",
            "data": {
                "bus_list": busList,
                "station_list": stationList
            }
        }
    except:
        return {
            "status": 404,
            "message": "Not found"
        }


@app.put("/api/v1/feedback")
def put_feedback(item: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return create_feedback(db, item)