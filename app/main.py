from fastapi import FastAPI
from kubernetes import client
from .db_helper import get_image_manifest, get_flags
from .config import KUBERNETES_KEY, KUBERNETES_URL, REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_USER, REDIS_PASSWORD
from pydantic import BaseModel
import redis
from .config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
from .shared_models.db_connect import Database
import json

db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)

app = FastAPI()





def get_k8s_config():
    configuration = client.Configuration()
    configuration.api_key['authorization'] = KUBERNETES_KEY
    configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.host = KUBERNETES_URL
    configuration.verify_ssl = False

    v1 = client.CoreV1Api(client.ApiClient(configuration))
    return v1

def create_namespace(name: str):
    v1 = get_k8s_config()
    body = client.V1Namespace(metadata=client.V1ObjectMeta(name=name))
    return v1.create_namespace(body)

def namespace_exists(name: str):
    v1 = get_k8s_config()
    namespaces = v1.list_namespace()
    for ns in namespaces.items:
        if ns.metadata.name == name:
            return True
    return False


class Data(BaseModel):
    user_id: int
    image_id: int

def create_in_k8s(user_id, image_id):
    if not namespace_exists(user_id):
        create_namespace(user_id)
    manifest = get_image_manifest(db, image_id)
    v1 = get_k8s_config()
    return v1.create_namespaced_pod(user_id, manifest)

def get_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, username=REDIS_USER, password=REDIS_PASSWORD)

def create_in_redis(user_id, image_id):
    r = get_redis()

    # add image_id to redis zset of user id
    r.sadd(user_id, image_id)

def create_details(image_id):
    flags = get_flags(image_id)
    r = get_redis()
    r.hset(image_id, "flags", json.dumps(flags))


@app.post("/")
def create_instance(data: Data):
    user_id = data.user_id
    image_id = data.image_id
    create_in_k8s(user_id, image_id)
    create_in_redis(user_id, image_id)
    create_details(image_id)
    return {"status": "success"}

