from . import _Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


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
