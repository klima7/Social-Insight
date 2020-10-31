from . import _Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(_Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    mail = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    packs = relationship("Pack", backref="user")

    def __repr__(self):
        return f"<User(id={self.id}, mail='{self.mail}', packs={self.packs})>"


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
