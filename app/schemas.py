from pydantic import BaseModel

# 클라이언트로부터의 입력 명시
## 피드백 테이블
class FeedbackBase(BaseModel):
    miss_time: int = 0

class FeedbackCreate(FeedbackBase):
    station_id: str
    bus_id: str

class Feedback(FeedbackBase):
    id: int

    class Config:
        orm_mode = True

## 버스 테이블
class BusBase(BaseModel):
    type: str
    area: str | None = None
    num: str

class BusCreate(BusBase):
    id: str
    sp_id: str
    ep_id: str
    fd_time: int | None = None
    ld_time: int | None = None
    interval_time: int | None = None
    interval_haltime: int | None = None

class Bus(BusBase):
    id: str

    class Config:
        orm_mode = True

## 정류장 테이블
class StationBase(BaseModel):
    name: str
    city: int

class StationCreate(StationBase):
    id: str
    lat: float
    lon: float

class Station(StationBase):
    id: str

    class Config:
        orm_mode = True

## 버스-정류장 매칭 테이블
class RouteBase(BaseModel):
    station_id: str
    bus_id: str
    miss_time: int = 0

class RouteCreate(RouteBase):
    pass

class Route(RouteBase):
    class Config:
        orm_mode = True