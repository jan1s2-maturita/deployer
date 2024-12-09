from fastapi import FastAPI
from kubernetes import client
from .config import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_USER, REDIS_PASSWORD, KUBERNETES_KEY, KUBERNETES_URL
from .shared_models.k8s_helper import Kubernetes
from pydantic import BaseModel
from .config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
from .shared_models.db_connect import Database
from .shared_models.redis_helper import RedisConnector
import json


app = FastAPI()

db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)
kube = Kubernetes(KUBERNETES_KEY, KUBERNETES_URL)
redis_conn = RedisConnector(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, user=REDIS_USER, password=REDIS_PASSWORD)

class Data(BaseModel):
    user_id: int
    image_id: int




@app.post("/")
def create_instance(data: Data):
    user_id = data.user_id
    image_id = data.image_id
    kube.create_in_k8s(db=db, user_id=user_id, image_id=image_id)
    redis_conn.create_instance(user_id=user_id, image_id=image_id)
    return {"status": "success"}

