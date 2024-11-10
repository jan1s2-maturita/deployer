from fastapi import FastAPI
from kubernetes import client
from .db_helper import get_image_manifest, get_flags
from .config import DEPLOY_NAMESPACE, KUBERNETES_KEY, KUBERNETES_URL, REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_USER, REDIS_PASSWORD
from pydantic import BaseModel
import redis
app = FastAPI()


def get_k8s_config():
    configuration = client.Configuration()
    configuration.api_key['authorization'] = KUBERNETES_KEY
    configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.host = KUBERNETES_URL
    configuration.verify_ssl = False

    v1 = client.CoreV1Api(client.ApiClient(configuration))
    return v1


class Data(BaseModel):
    user_id: int
    image_id: int

def create_in_k8s(image_id):
    manifest = get_image_manifest(image_id)
    v1 = get_k8s_config()
    return v1.create_namespaced_pod(DEPLOY_NAMESPACE, manifest)

def create_in_redis(user_id, image_id):
    assert (REDIS_HOST and REDIS_PORT and REDIS_DB and REDIS_USER and REDIS_PASSWORD)
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, username=REDIS_USER, password=REDIS_PASSWORD)

    # add image_id to redis zset of user id
    r.zadd(user_id, {image_id: 0})

@app.post("/create_instance/")
def create_instance(data: Data):
    user_id = data.user_id
    image_id = data.image_id
    create_in_k8s(image_id)
    create_in_redis(user_id, image_id)
    return {"status": "success"}

