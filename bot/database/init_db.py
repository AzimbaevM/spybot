from .db import Base, engine
from .models import Player, Game

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("DB initialized")
