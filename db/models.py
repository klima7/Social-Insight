from datetime import datetime

from flask_login import UserMixin
from flask_babel import _
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Table
from sqlalchemy.types import PickleType
from werkzeug.security import generate_password_hash, check_password_hash

from db import *
from . import _Base
from util import _t, remove_accents


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
        return f"<User(id={self.id})>"

    def is_admin(self):
        return self.email == config.MAIL_USERNAME

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

    @staticmethod
    def get_user_from_confirm_token(token):
        s = Serializer(config.SECRET_KEY)
        try:
            data = s.loads(token.encode('utf-8'))
            return db_session.query(User).filter_by(id=data.get('confirm')).first()
        except:
            return None

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

    STATUS_PENDING = _t('pending')
    STATUS_PROCESSING = _t('processing')
    STATUS_SUCCESS = _t('success')
    STATUS_FAILURE = _t('failure')

    def __repr__(self):
        return f"<Pack(id={self.id})>"


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
    data_extended = Column(PickleType)
    public = Column(Boolean, default=False)
    collations = relationship('Collation',
                              secondary=collation_entries,
                              backref=backref('graphs', lazy='select'),
                              lazy='select')

    @property
    def name_trans(self):
        return _(self.name)

    @property
    def name_without_accents(self):
        return remove_accents(self.name_trans)

    @property
    def category_trans(self):
        return _(self.category)

    @property
    def category_without_accents(self):
        return remove_accents(self.category_trans)

    def get_data(self, extended=False):
        if extended and self.data_extended is not None:
            return self.data_extended
        else:
            return self.data

    def render_png(self, path):
        import frontend.render as render
        return render.render_chart_png(self, path)

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

    def size(self):
        return len(self.graphs)

    def __repr__(self):
        return f"<Collation(id={self.id})>"


class Global(_Base):
    __tablename__ = 'global'

    id = Column(Integer, primary_key=True)
    christmas_event = Column(Boolean, default=True)

    @staticmethod
    def create():
        g = db_session.query(Global).first()
        if g is None:
            g = Global()
            db_session.add(g)
            db_session.commit()

    @staticmethod
    def get_christmas_event():
        g = db_session.query(Global).first()
        return g.christmas_event

    def __repr__(self):
        return f"<Global(id={self.id})>"


class Message(_Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender = Column(String)
    topic = Column(String)
    content = Column(String)
    date = Column(DateTime(), default=datetime.utcnow)
    language = Column(String)

    def __repr__(self):
        return f"<Message(id={self.id})>"


class File(_Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    progress = Column(Integer, default=0)
    ready = Column(Boolean, default=False)

    def __repr__(self):
        return f"<File(id={self.id})>"


