import os
DEBUG = True
DEPLOY_NAMESPACE = 'dev' if DEBUG else os.environ.get('DEPLOY_NAMESPACE')
KUBERNETES_KEY = 'k8s_key' if DEBUG else os.environ.get('KUBERNETES_KEY')
KUBERNETES_URL = 'https://kubernetes.default.svc.cluster.local'

PUBLIC_KEY = 'public.pem' if DEBUG else os.environ.get('PUBLIC_KEY')

DB_HOST = 'db' if DEBUG else os.environ.get('DB_HOST')
DB_PORT = 5432 if DEBUG else os.environ.get('DB_PORT')
DB_USER = 'postgres' if DEBUG else os.environ.get('DB_USER')
DB_PASS = 'postgres' if DEBUG else os.environ.get('DB_PASS')
DB_NAME = 'postgres' if DEBUG else os.environ.get('DB_NAME')


REDIS_HOST = 'redis' if DEBUG else os.environ.get('REDIS_HOST')
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_USER = 'redis_user' if DEBUG else os.environ.get('REDIS_USER')
REDIS_PASSWORD = 'redis_password' if DEBUG else os.environ.get('REDIS_PASSWORD')
