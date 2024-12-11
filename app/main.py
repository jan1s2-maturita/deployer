from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from .config import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_USER, REDIS_PASSWORD, KUBERNETES_KEY, KUBERNETES_URL, PUBLIC_KEY_PATH
from .config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
from .shared_models import Kubernetes, RedisConnector, Database
from jwt import decode

kube: Kubernetes
r: RedisConnector
db: Database

@asynccontextmanager
async def init(app: FastAPI):
    global kube
    global r
    global db
    kube = Kubernetes(key=KUBERNETES_KEY, url=KUBERNETES_URL)
    r = RedisConnector(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, user=REDIS_USER)
    db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)
    yield

app = FastAPI()


class Data(BaseModel):
    # user_id: int
    image_id: int

@app.post("/")
def create_instance(x_token: Annotated[str, Header()], data: Data):
    payload = None
    try:
        with open(PUBLIC_KEY_PATH, 'r') as f:
            public_key = f.read()
            payload = decode(x_token, public_key, algorithms=['RS256'])
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload["id"]
    image_id = data.image_id
    kube.create_in_k8s(db=db, user_id=user_id, image_id=image_id)
    r.create_instance(user_id=user_id, image_id=image_id)
    return {"status": "success"}

