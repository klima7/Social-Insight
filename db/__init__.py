from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import config
from .constants import GraphName, PackStatus


_engine = create_engine(f'sqlite:///{config.DATABASE_LOCATION}', echo=config.DATABASE_DEBUG, connect_args={"check_same_thread": False})
_Base = declarative_base()
_Session = scoped_session(sessionmaker(bind=_engine))
db_session = _Session()

# Import musi być tutaj (nie u góry) by uniknąć zależności cyklicznych
from .models import *

_Base.metadata.create_all(_engine)


def clean_db():
    _Base.metadata.drop_all(bind=_engine)
    _Base.metadata.create_all(_engine)





