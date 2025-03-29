import sqlalchemy # type: ignore
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import declarative_base # type: ignore
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker


from config import config # type: ignore

DATABASE_URL = "postgresql://%s:%s@%s:%s/%s" % (
    config["database"]["user"],
    config["database"]["password"],
    config["database"]["host"],
    config["database"]["port"],
    config["database"]["dbname"]
)

engine = create_engine(DATABASE_URL)

DeclarativeBase = declarative_base()

class User(DeclarativeBase): # type: ignore
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
    salt = Column(String)
    created_at = Column(DateTime())
    expires_at = Column(DateTime())

class Token(DeclarativeBase): # type: ignore
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    token = Column(String)
    created_at = Column(DateTime())
    expires_at = Column(DateTime())

# DeclarativeBase.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 'Hello, PostgreSQL!'"))
        print(result.fetchone()[0])