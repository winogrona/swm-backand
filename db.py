import sqlalchemy # type: ignore
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import declarative_base # type: ignore
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker

from enum import Enum

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

class Materials(str, Enum):
    PLASTIC = "plastic"
    METAL = "metal"
    GLASS = "glass"

class Category(str, Enum):
    # Categories for the items
    CLOTHING = "clothing"
    TOYS = "toys"
    KITCHENWARE = "kitchenware"  # Dishes, forks, spoons, containers, kitchen towels etc.
    FURNITURE = "furniture"
    THREE_D_PRINTING = "3dprinting"  # Filaments
    OTHER = "other"  # Paper

class Products(DeclarativeBase): # type: ignore
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_picture_url = Column(String, nullable=False)
    product_picture_url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)
    percent_recycled = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    materials = Column(String, nullable=False)

    def __todict__(self) -> dict:
        return {
            "id": self.id,
            "storePictureUrl": self.storePictureUrl,
            "productPictureUrl": self.productPictureUrl,
            "name": self.name,
            "description": self.description,
            "cost": self.cost,
            "percentRecycled": self.percentRecycled,
            "category": self.category,
            "materials": self.materials
        }
    
class Machines(DeclarativeBase): # type: ignore
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def __todict__(self) -> dict:
        return {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 'Hello, PostgreSQL!'"))
        print(result.fetchone()[0])