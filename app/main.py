from typing import Union
from fastapi import Depends, FastAPI, HTTPException
from mangum import Mangum
from sqlalchemy.orm import Session

import crud, models, schemas
from api.station import *
from database import SessionLocal, engine

from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

#models.Base.metadata.create_all(bind=engine)
openApiEndpoint = "http://apis.data.go.kr/1613000/BusSttnInfoInqireService"


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
    url = f"{openApiEndpoint}/getCrdntPrxmtSttnList?serviceKey={os.environ["data_go_kr_key"]}&_type=json&gpsLati={lat}&gpsLong={lon}"
    return await get_station(url, skip)
