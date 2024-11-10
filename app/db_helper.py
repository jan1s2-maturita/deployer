from sqlalchemy import create_engine, select
from .config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
from .shared_models.model import Flags, User, Base

# def get_db_connection():
    # return psycopg2.connect(
        # host=DB_HOST,
        # port=DB_PORT,
        # user=DB_USER,
        # password=DB_PASS,
        # database=DB_NAME
    # )
# connect ORM
def get_db_connection():
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    Base.metadata.create_all(engine)
    return engine

def get_image_manifest(image_id):
    conn = get_db_connection()
    # use sql alchemy
    result = None
    with conn.connect() as connection:
        stmt = select([Flags]).where(Flags.id == image_id)
        result = connection.execute(stmt)
    return result.fetchone()

def get_flags(id: int):
    conn = get_db_connection()
    result = None
    with conn.connect() as connection:
        stmt = select([Flags]).where(Flags.pod_id == id)
        result = connection.execute(stmt)
    return result.fetchall()
