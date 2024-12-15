from sqlalchemy import Column, Integer, String, Table, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserFighter(Base):
    __tablename__ = "user_fighters"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    fighter_id = Column(Integer, ForeignKey("fighters.id"), primary_key=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="user_fighters")
    fighter = relationship("Fighter", back_populates="user_fighters")


class FightResult(Base):
    __tablename__ = "fight_results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    fighter_id = Column(Integer, ForeignKey("fighters.id"))  # changed from fighter
    opponent_id = Column(Integer, ForeignKey("fighters.id"))  # changed from opponent
    is_user_win = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="fight_results")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    next_win_count = Column(Integer, default=3)
    notifications_enabled = Column(Boolean, default=False)

    user_fighters = relationship("UserFighter", back_populates="user")
    fight_results = relationship("FightResult", back_populates="user")


class Fighter(Base):
    __tablename__ = "fighters"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    attack_power = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    is_default = Column(Boolean, default=False)
    user_fighters = relationship("UserFighter", back_populates="fighter")

    def __repr__(self):
        return f"{self.name} [{self.icon}]\nattack {self.attack_power}\n{self.description})"
