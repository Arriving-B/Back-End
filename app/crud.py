from sqlalchemy.orm import Session
import models, schemas

# 클라이언트로부터 받은 데이터를 기입
## 피드백
def get_feedbacks(db: Session, station_id: str, bus_id: str):
    return db.query(models.Feedback).filter(
        models.Feedback.station_id == station_id &
        models.Feedback.bus_id == bus_id    
    ).all()

def get_feedback_by_id(db: Session, id: int):
    return db.query(models.Feedback).filter(
        models.Feedback.id == id
    ).first()

def get_all_feedbacks(db: Session, skip: int = 0, limit: int = 100):
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
