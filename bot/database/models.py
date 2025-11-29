from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .db import Base
from datetime import datetime

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True)  # telegram user id
    username = Column(String, index=True)
    money = Column(Integer, default=100)
    gems = Column(Integer, default=0)
    protection = Column(Integer, default=0)
    documents = Column(Integer, default=0)
    active_role = Column(String, nullable=True)  # можно хранить текущую роль (если нужно)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Player {self.username} ({self.tg_id})>"

class GameHistory(Base):
    __tablename__ = "game_history"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    result = Column(String)  # краткий текст результата
    details = Column(String) # json/text с деталями (ролями, слова и т.д.)

    def __repr__(self):
        return f"<GameHistory {self.chat_id} @ {self.created_at}>"
