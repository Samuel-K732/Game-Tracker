from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, Date, LargeBinary, ForeignKey
import enum


Base = declarative_base()

class ReviewType(enum.Enum):
    BAD = "Bad"
    OKAY = "Okay"
    GOOD = "Good"
    AMAZING = "Amazing"

class Game(Base):
    __tablename__ = "Games"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    image = Column(LargeBinary)
    time_spent = Column(String, nullable=False)
    dlc = Column(String)
    achievements = Column(String)
    date = Column(Date, nullable=False)
    review = Column(String, nullable=False)

    year = relationship("Year", back_populates="game", cascade="all, delete")

class Year(Base):
    __tablename__ = "Years"
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    game_id = Column(Integer, ForeignKey("Games.id"))
    game_name = Column(String)

    game = relationship("Game", back_populates="year")
