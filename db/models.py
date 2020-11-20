from datetime import datetime

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
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
    packs = relationship("Pack", backref="user")

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
    done = Column(Boolean)

    chart1 = Column(String)
    chart2 = Column(String)
    chart3 = Column(String)
    chart4 = Column(String)

    def __repr__(self):
        return f"<Pack(id={self.id}, userid='{self.userid}' done={self.done})>"
