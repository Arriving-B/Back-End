from sqlalchemy.orm import Session
import models, schemas

# 클라이언트로부터 받은 데이터를 기입
## 피드백
def get_feedback(db: Session, station_id: str, bus_id: str):
    return db.query(models.Feedback).filter(
        models.Feedback.station_id == station_id &
        models.Feedback.bus_id == bus_id    
    ).first()

def get_feedback_by_id(db: Session, id: int):
    return db.query(models.Feedback).filter(
        models.Feedback.id == id
    ).first()

def get_feedbacks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Feedback).offset(skip).limit(limit).all()

def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    feedback_db_create = models.Feedback(
        miss_time = feedback.miss_time,
        station_id = feedback.station_id,
        bus_id = feedback.bus_id
    )
    db.add(feedback_db_create)
    db.commit()
    db.refresh(feedback_db_create)
    print("Feedback Created : ", feedback_db_create)
    return feedback_db_create

## 버스
def get_bus(db: Session, id: str):
    return db.query(models.Bus).filter(
        models.Bus.id == id
    ).first()

def get_buses_by_num(db: Session, num: str):
    return db.query(models.Bus).filter(
        models.Bus.num == num
    ).all()

def get_buses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bus).offset(skip).limit(limit).all()

def create_bus(db: Session, bus: schemas.BusCreate):
    bus_db_create = models.Bus(
        id = bus.id,
        type = bus.type,
        area = bus.area,
        num = bus.num,
        sp_id = bus.sp_id,
        ep_id = bus.ep_id,
        fd_time = bus.fd_time,
        ld_time = bus.ld_time,
        interval_time = bus.interval_time,
        interval_haltime = bus.interval_haltime
    )
    db.add(bus_db_create)
    db.commit()
    db.refresh(bus_db_create)
    print("Bus Created : ", bus_db_create)
    return bus_db_create

## 정류장
def get_station(db: Session, id: str):
    return db.query(models.Station).filter(
        models.Station.id == id
    ).first()

def get_station_by_name_and_city(db: Session, name: str, city: int):
    return db.query(models.Station).filter(
        models.Station.name == name &
        models.Station.city == city
    ).first()

def get_stations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Station).offset(skip).limit(limit).all()

def create_station(db: Session, station: schemas.StationCreate):
    station_db_create = models.Station(
        id = station.id,
        name = station.name,
        city = station.city,
        lat = station.lat,
        lon = station.lon
    )
    db.add(station_db_create)
    db.commit()
    db.refresh(station_db_create)
    print("Station Created : ", station_db_create)
    return station_db_create

## 버스-정류장
def get_bus_list(db: Session, station_id: str):
    return db.query(models.Route).filter(
        models.Route.station_id == station_id
    ).all()

def get_route(db: Session, bus_id: str):
    return db.query(models.Route).filter(
        models.Route.bus_id == bus_id
    ).all()

def get_missTime(db: Session, station_id: str, bus_id: str):
    return db.query(models.Bus).filter(
        models.Route.station_id == station_id &
        models.Route.bus_id == bus_id
    ).first()

def create_node(db: Session, node: schemas.RouteCreate):
    node_db_create = models.Route(
        station_id = node.station_id,
        bus_id = node.bus_id,
        miss_time = node.miss_time
    )
    db.add(node_db_create)
    db.commit()
    db.refresh(node_db_create)
    print("Node Created : ", node_db_create)
    return node_db_create

def update_missTime(db: Session, node: models.Route, new_miss_time: int):
    node_db_update = db.query(models.Route).filter(models.Route == node).first()
    node_db_update.miss_time = new_miss_time
    db.commit()
    print("Node Updated : ", node_db_update)
    return node_db_update

def delete_route(db: Session, node: models.Route):
    node_db_delete = db.query(models.Route).filter(models.Route == node).first()
    db.delete(node_db_delete)
    db.commit()
    print("Node Deleted : ", node_db_delete)
    return node_db_delete