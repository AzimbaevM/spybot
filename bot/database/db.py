from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

Base = declarative_base()
engine = create_engine("sqlite:///bot/database/game.db")
Session = sessionmaker(bind=engine)
session = Session()

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(String)

def init_db():
    os.makedirs("bot/database", exist_ok=True)
    Base.metadata.create_all(engine)
    print("База данных создана.")
