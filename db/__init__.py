from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlite3 import Connection as SQLite3Connection
from config import config


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


_engine = create_engine(f'sqlite:///{config.DATABASE_LOCATION}', echo=config.DATABASE_DEBUG, connect_args={"check_same_thread": False})
_Base = declarative_base()
_Session = scoped_session(sessionmaker(bind=_engine))
db_session = _Session()

# Import musi być tutaj (nie u góry) by uniknąć zależności cyklicznych
from .models import *

_Base.metadata.create_all(_engine)


def _prepare():
    Global.create()

    try:
        user = User(email='user@test.com', confirmed=True)
        user.password = 'password'
        db_session.add(user)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()

    try:
        user = User(email='user2@test.com', confirmed=False)
        user.password = 'password'
        db_session.add(user)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()

    try:
        user = User(email=config.MAIL_USERNAME, confirmed=True)
        user.password = config.MAIL_PASSWORD
        db_session.add(user)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()


def clean_db():
    _Base.metadata.drop_all(bind=_engine)
    _Base.metadata.create_all(_engine)


def example_pack_update():
    import os
    import threading
    import analytics

    db_session.query(Pack).filter_by(example=True).delete()
    db_session.commit()

    if not os.path.exists('example.zip'):
        raise FileNotFoundError()

    pack = Pack(status=Pack.STATUS_PENDING, example=True)
    db_session.add(pack)
    db_session.commit()

    thread = threading.Thread(target=analytics.analyse, args=[pack.id, 'example.zip', False])
    thread.start()


_prepare()


