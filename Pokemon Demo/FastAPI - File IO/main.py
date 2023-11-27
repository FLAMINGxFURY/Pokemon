from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel

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

# Load data or create empty dataframe if file not found
try:
	df = pd.read_csv('pokemon.csv')
except:
	df = pd.DataFrame(columns=['id', 'name', 'imageurl'])

# Define pokemon model using Pydantic's structure for serialization and deserialization 
class Pokemon(BaseModel):
	id: int
	name: str
	imageurl: str

# Define pokemon list model
class PokemonList(BaseModel):
	pokemon: list[Pokemon]

# GET requests | orient='records' returns a list of dictionaries which is serialized by FastAPI to JSON
@app.get("/count")
async def get_count():
	return len(df)

@app.get("/pokemon")
async def get_pokemon():
	return PokemonList(pokemon=df.to_dict(orient='records'))

@app.get("/pokemon/{id}")
async def get_pokemon_by_id(id: int):
	# Filter the dataframe by the supplied id. If there is no matching id, 'pokemon' will be an empty dataframe
	pokemon = df[df['id'] == id]

	if pokemon.empty:
		raise HTTPException(status_code=404, detail="Pokemon not found")

	return pokemon.to_dict(orient='records')[0]

# POST request
@app.post("/pokemon")
async def add_pokemon(pokemon: Pokemon):
	# make df globally available so that our uvicorn server can access it
	global df
	
	# Check if the pokemon already exists in the dataframe
	if pokemon.id in df['id'].values:
		raise HTTPException(status_code=400, detail="Pokemon already exists")

	## The below operations are for updating the csv file once the operation is complete
	# Create a new DataFrame with the new pokemon
	new_pokemon_df = pd.DataFrame([pokemon.model_dump()])

	# Concatenate the new DataFrame with the existing DataFrame
	df = pd.concat([df, new_pokemon_df], ignore_index=True)

	# Save the dataframe to a csv file
	df.to_csv('pokemon.csv', index=False)

	return pokemon

# PUT request
@app.put("/pokemon/{id}")
async def update_pokemon(id: int, pokemon: Pokemon):
	# make df globally available so that our uvicorn server can access it
	global df

	# Check if the pokemon already exists in the dataframe
	if id not in df['id'].values:
		raise HTTPException(status_code=404, detail="Pokemon not found")

	## The below operations are for updating the csv file once the operation is complete
	# Update the pokemon in the dataframe
	df.loc[df['id'] == id, ['name', 'imageurl']] = [pokemon.name, pokemon.imageurl]

	# Save the dataframe to a csv file
	df.to_csv('pokemon.csv', index=False)

	return pokemon

# PATCH requests
# Patch the name of a pokemon
@app.patch("/pokemon/{id}/name")
async def update_pokemon_name(id: int, name: str):
	# make df globally available so that our uvicorn server can access it
	global df

	# Check if the pokemon already exists in the dataframe
	if id not in df['id'].values:
		raise HTTPException(status_code=404, detail="Pokemon not found")

	## The below operations are for updating the csv file once the operation is complete
	# Update the pokemon in the dataframe
	df.loc[df['id'] == id, ['name']] = [name]

	# Save the dataframe to a csv file
	df.to_csv('pokemon.csv', index=False)

	return name

# Patch the imageurl of a pokemon
@app.patch("/pokemon/{id}/imageurl")
async def update_pokemon_imageurl(id: int, imageurl: str):
	# make df globally available so that our uvicorn server can access it
	global df

	# Check if the pokemon already exists in the dataframe
	if id not in df['id'].values:
		raise HTTPException(status_code=404, detail="Pokemon not found")

	## The below operations are for updating the csv file once the operation is complete
	# Update the pokemon in the dataframe
	df.loc[df['id'] == id, ['imageurl']] = [imageurl]

	# Save the dataframe to a csv file
	df.to_csv('pokemon.csv', index=False)

	return imageurl

# DELETE request
@app.delete("/pokemon/{id}")
async def delete_pokemon(id: int):
	# make df globally available so that our uvicorn server can access it
	global df

	# Check if the pokemon already exists in the dataframe
	if id not in df['id'].values:
		raise HTTPException(status_code=404, detail="Pokemon not found")

	## The below operations are for updating the csv file once the operation is complete
	# Delete the pokemon from the dataframe
	df = df[df['id'] != id]

	# Save the dataframe to a csv file
	df.to_csv('pokemon.csv', index=False)

	# Return a success message
	return { 'message': 'Pokemon deleted' }