from typing import Union
from fastapi import Depends, FastAPI, HTTPException
from mangum import Mangum
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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
async def read_root(db: Session = Depends(get_db)):
    return {"Hello": "World"}


@app.get("/items")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}