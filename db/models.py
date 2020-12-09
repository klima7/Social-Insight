from datetime import datetime

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Table
from sqlalchemy.types import PickleType
from werkzeug.security import generate_password_hash, check_password_hash

from db import *
from . import _Base


class User(_Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    confirmed = Column(Boolean, default=False)
    registration_data = Column(DateTime(), default=datetime.utcnow)
    packs = relationship("Pack", backref="user", lazy='select')
    collations = relationship("Collation", backref="user", lazy='select')

    def __repr__(self):
        return f"<User(id={self.id}, mail='{self.mail}', packs={self.packs})>"

    @property
    def password(self):
        raise AttributeError('Password is read only')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        s = Serializer(config.SECRET_KEY, config.CONFIRMATION_TIME*60)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(config.SECRET_KEY)
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db_session.add(self)
        return True

    def generate_reset_token(self):
        s = Serializer(config.SECRET_KEY, config.PASSWORD_CHANGE_TIME)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(config.SECRET_KEY)
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = db_session.query(User).filter_by(id=data.get('reset')).first()
        if user is None:
            return False
        user.password = new_password
        db_session.add(user)
        return True


class Pack(_Base):
    __tablename__ = 'packs'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('users.id'))
    name = Column(String, default='Pack')
    status = Column(String)
    creation_date = Column(DateTime(), default=datetime.utcnow)
    graphs = relationship("Graph", backref="pack", lazy='dynamic', passive_deletes=True)
    example = Column(Boolean, default=False)

    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_SUCCESS = 'success'
    STATUS_FAILURE = 'failure'

    def __repr__(self):
        return f"<Pack(id={self.id}, userid='{self.userid}' done={self.done})>"


collation_entries = Table('collation_entries', _Base.metadata,
    Column('collation_id', Integer, ForeignKey('collations.id')),
    Column('graph_id', Integer, ForeignKey('graphs.id'))
)


class Graph(_Base):
    __tablename__ = 'graphs'

    id = Column(Integer, primary_key=True)
    packid = Column(Integer, ForeignKey('packs.id', ondelete='CASCADE'))
    name = Column(String)
    category = Column(String)
    data = Column(PickleType)
    public = Column(Boolean, default=False)
    collations = relationship('Collation',
                              secondary=collation_entries,
                              backref=backref('graphs', lazy='select'),
                              lazy='select')

    def get_name(self):
        from analytics import get_translated_graph_name
        return get_translated_graph_name(self.name)

    def __repr__(self):
        return f"<Graph(id={self.id})>"


class Collation(_Base):
    __tablename__ = 'collations'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('users.id'))
    name = Column(String, default='Collation')
    creation_date = Column(DateTime(), default=datetime.utcnow)

    def contains(self, graph):
        for g in self.graphs:
            if g == graph:
                return True
        return False

    def __repr__(self):
        return f"<Collation(id={self.id})>"


