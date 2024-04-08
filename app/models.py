from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


user_fighters = Table('user_fighters', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('fighter_id', Integer, ForeignKey('fighters.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    fighters = relationship('Fighter', secondary=user_fighters, backref='users')


class Fighter(Base):
    __tablename__ = 'fighters'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    attack_power = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    is_default = Column(Boolean, default=False)

    def __repr__(self):
        return f"{self.name} [{self.icon}]\nattack {self.attack_power}\n{self.description})"