import os
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
DEPLOY_NAMESPACE = os.environ.get('DEPLOY_NAMESPACE', 'dev')
KUBERNETES_KEY = os.environ.get('KUBERNETES_KEY', 'k8s_key')
KUBERNETES_URL = os.environ.get('KUBENETES_URL', 'https://kubernetes.default.svc.cluster.local')

PUBLIC_KEY_PATH = os.environ.get('PUBLIC_KEY_PATH', 'public.pem')

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = int(os.environ.get('DB_PORT', '5432'))
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'postgres')
DB_NAME = os.environ.get('DB_NAME', 'postgres')


REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_DB = int(os.environ.get('REDIS_DB', '0'))
REDIS_USER = os.environ.get('REDIS_USER', 'redis_user')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', 'redis_password')
ZSET_NAME = 'deployed_instances'
