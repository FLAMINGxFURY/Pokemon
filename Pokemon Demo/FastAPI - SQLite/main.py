from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Imports from our dbmodel.py file
from dbmodel import Base, Pokemon, PokemonCreate, PokemonRead

app = FastAPI()

# because we are hosting both Blazor and FastAPI on the same server (localhost), we need to enable CORS 
# to allow the Blazor client to make requests to the FastAPI server
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"], # set to * here to allow all origins because Blazor does not have a set origin port for all users. 
						 # Ideally, you would set this to the port that Blazor is running on (e.g. http://localhost:7134 for me)
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Set up our local database session
SQLALCHEMY_DATABASE_URL = "sqlite:///./pokemon.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This binds our ORM class models
Base.metadata.create_all(bind=engine)

# This function will serve as a Dependency Inversion for our db connection at our FastAPI endpoints.
# Each endpoint function will have this connection passed in as a parameter using the Depends() function.
# This is similar to Blazor's @inject directive for components.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
      
# GET requests
@app.get("/count")
async def get_count(db: Session = Depends(get_db)):
    return db.query(Pokemon).count()

@app.get("/pokemon")
async def get_pokemon(db: Session = Depends(get_db)):
    pokemon_list = db.query(Pokemon).all()
    
    # Here, I'm using a simple list comprehension to create the JSON response. There's a bit more overhead if we 
    # want to use a Pydantic model for the list in conjunction with the PokemonRead model.
    return [{"id": pokemon.id, "name": pokemon.name, "imageurl": pokemon.imageurl} for pokemon in pokemon_list]

@app.get("/pokemon/{id}")
async def get_pokemon_by_id(id: int, db: Session = Depends(get_db)):
    pokemon = db.query(Pokemon).filter(Pokemon.id == id).first()

    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    return pokemon

# POST request
@app.post("/pokemon")
async def add_pokemon(pokemon: PokemonCreate, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Pokemon).filter(Pokemon.id == pokemon.id).first() is not None:
        raise HTTPException(status_code=400, detail="Pokemon already exists")

    # Create a new Pokemon object using the PokemonCreate model
    new_pokemon = Pokemon(id=pokemon.id, name=pokemon.name, imageurl=pokemon.imageurl)

    # Add the new Pokemon object to the database
    db.add(new_pokemon)
    db.commit()
    db.refresh(new_pokemon)

    # Return the new Pokemon object using the PokemonRead model
    return new_pokemon

# PUT request
@app.put("/pokemon/{id}")
async def update_pokemon(id: int, pokemon: PokemonCreate, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Pokemon).filter(Pokemon.id == id).first() is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    # Update the Pokemon object in the database
    db.query(Pokemon).filter(Pokemon.id == id).update({Pokemon.name: pokemon.name, Pokemon.imageurl: pokemon.imageurl})
    db.commit()

    # Return the updated Pokemon object using the PokemonRead model
    return db.query(Pokemon).filter(Pokemon.id == id).first()

# PATCH requests
@app.patch("/pokemon/{id}/name")
async def update_pokemon_name(id: int, name: str, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Pokemon).filter(Pokemon.id == id).first() is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    # Update the Pokemon object in the database
    db.query(Pokemon).filter(Pokemon.id == id).update({Pokemon.name: name})
    db.commit()

    # Return the updated Pokemon object using the PokemonRead model
    return db.query(Pokemon).filter(Pokemon.id == id).first()

@app.patch("/pokemon/{id}/imageurl")
async def update_pokemon_imageurl(id: int, imageurl: str, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Pokemon).filter(Pokemon.id == id).first() is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    # Update the Pokemon object in the database
    db.query(Pokemon).filter(Pokemon.id == id).update({Pokemon.imageurl: imageurl})
    db.commit()

    # Return the updated Pokemon object using the PokemonRead model
    return db.query(Pokemon).filter(Pokemon.id == id).first()

# DELETE request
@app.delete("/pokemon/{id}")
async def delete_pokemon(id: int, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Pokemon).filter(Pokemon.id == id).first() is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    # Delete the Pokemon object from the database
    db.query(Pokemon).filter(Pokemon.id == id).delete()
    db.commit()

    # Return a success message
    return {"message": "Pokemon deleted"}