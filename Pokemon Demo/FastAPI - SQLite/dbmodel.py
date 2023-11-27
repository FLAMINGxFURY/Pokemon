from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# SQLAlchemy setup
Base = declarative_base()

# Database model for Pokémon
class Pokemon(Base):
    __tablename__ = 'pokemon'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    imageurl = Column(String)

    # This is the same as overriding ToString() in C#
    def __repr__(self):
        return f"<Pokemon(pokedex_number={self.id}, name='{self.name}', imageurl='{self.imageurl}')>"

# This is similar to Microsoft.Data.Sqlite - we need an object to represent the database record
class PokemonCreate(BaseModel):
    id: int
    name: str
    imageurl: str

# Here, we set the orm flag so that a database record can be converted to a Pydantic model on a read
class PokemonRead(PokemonCreate):
    class Config:
        orm_mode = True
