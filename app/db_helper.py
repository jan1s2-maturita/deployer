from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from .config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
from .shared_models.model import Flags, User, Base
from .shared_models.db_connect import Database

# def get_db_connection():
    # return psycopg2.connect(
        # host=DB_HOST,
        # port=DB_PORT,
        # user=DB_USER,
        # password=DB_PASS,
        # database=DB_NAME
    # )
# connect ORM

def get_image_manifest(db: Database, image_id):
    conn: Session = db.get_session()
    # use sql alchemy
    result = conn.query(Flags).filter(Flags.id == image_id).first()
    return result


    # result = None
    # with conn.connect() as connection:
        # stmt = select([Flags]).where(Flags.id == image_id)
        # result = connection.execute(stmt)
    # return result.fetchone()

def get_flags(id: int):
    conn: Session = db.get_session()
    result = conn.query(Flags).filter(Flags.id == id).all()
    return result
