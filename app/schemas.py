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