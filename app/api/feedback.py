from sqlalchemy.orm import Session
import crud, schemas

def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    try: 
        crud.create_feedback(db, feedback)
        return {
            "status": 200,
            "message": "Feedback Create Success"
        }
    except:
        return {    
            "status": 404,
            "message": "Feedback Create Fail"
        }