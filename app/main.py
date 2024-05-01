import json
from typing import Union
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()
temp = -1

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

def handler(event, context): 
    Mangum(app)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!' + str(temp))
    }

if __name__ == "__main__":
    handler()