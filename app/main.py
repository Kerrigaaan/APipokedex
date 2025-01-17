from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
from . import database
from . import fonction

app = FastAPI()

class Pokemon(BaseModel):
    id: int
    name: str
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int
    image_url: str

class UpdatePokemon(BaseModel):
    name: str = None
    hp: int = None
    attack: int = None
    defense: int = None
    sp_attack: int = None
    sp_defense: int = None
    speed: int = None
    image_url: str = None

class PokemonType(BaseModel):
    type: str

class PokemonAbility(BaseModel):
    ability: str

# Crée un nouveau Pokémon dans la base de données.
@app.post("/pokemons/", response_model=dict)
def create_pokemon(pokemon: Pokemon):
    return fonction.create_pokemon(pokemon.dict())

# Ajoute un type à un Pokémon existant.
@app.post("/pokemons/{pokemon_id}/types", response_model=dict)
def add_type_to_pokemon(pokemon_id: int, type: PokemonType):
    return database.add_pokemon_type(pokemon_id, type.type)

# Ajoute une capacité à un Pokémon existant.
@app.post("/pokemons/{pokemon_id}/abilities", response_model=dict)
def add_ability_to_pokemon(pokemon_id: int, ability: PokemonAbility):
    return fonction.add_pokemon_ability(pokemon_id, ability.ability)

# Ajoute un commentaire à un Pokémon existant.
@app.post("/pokemons/comments/{pokemon_id}/", response_model=dict)
async def add_comment_to_pokemon(pokemon_id: int, comment: str):
    return fonction.add_comment_to_pokemon(pokemon_id, comment)

# Ajoute un Pokémon aux favoris.
@app.post("/pokemons/{pokemon_id}/favorite/", response_model=dict)
async def add_pokemon_to_favorites(pokemon_id: int):
    return fonction.add_pokemon_to_favorites(pokemon_id)

# Récupère un Pokémon en fonction de son identifiant.
@app.get("/pokemons/{pokemon_id}", response_model=dict)
def read_pokemon(pokemon_id: int):
    pokemon = fonction.get_pokemon_by_id(pokemon_id)
    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return pokemon

# Récupère tous les Pokémon avec une pagination.
@app.get("/pokemons/", response_model=list)
def read_pokemons(skip: int = 0, limit: int = 10):
    return fonction.get_all_pokemons(skip, limit)

# Recherche un Pokémon par son nom.
@app.get("/pokemons/search/{pokemon_name}", response_model=List[Pokemon])
def search_pokemon_by_name(pokemon_name: str):
    return fonction.search_pokemon_by_name(pokemon_name)

# Récupère tous les types de Pokémon disponibles.
@app.get("/types/", response_model=List[str])
def get_all_pokemon_types():
    return fonction.get_all_pokemon_types()

# Récupère toutes les capacités de Pokémon disponibles.
@app.get("/abilities/", response_model=List[str])
def get_all_pokemon_abilities():
    return fonction.get_all_pokemon_abilities()

# Recherche les Pokémon par type.
@app.get("/pokemons/type/{type_name}", response_model=List[Pokemon])
def search_pokemon_by_type(type_name: str):
    return fonction.search_pokemon_by_type(type_name)

# Recherche les Pokémon par capacité.
@app.get("/pokemons/ability/{ability_name}", response_model=List[Pokemon])
def search_pokemon_by_ability(ability_name: str):
    return fonction.search_pokemon_by_ability(ability_name)

# Récupère les capacités d'un Pokémon.
@app.get("/pokemons/{pokemon_id}/abilities", response_model=List[str])
def get_pokemon_abilities(pokemon_id: int):
    return fonction.get_pokemon_abilities(pokemon_id)

# Récupère les types d'un Pokémon.
@app.get("/pokemons/{pokemon_id}/types", response_model=List[str])
def get_pokemon_types(pokemon_id: int):
    return fonction.get_pokemon_types(pokemon_id)

# Récupère les statistiques de Pokémon.
@app.get("/pokemons/stats", response_model=dict)
def get_pokemon_stats():
    return fonction.get_pokemon_stats()

# Récupère un Pokémon aléatoire.
@app.get("/pokemons/random", response_model=Pokemon)
def get_random_pokemon():
    return fonction.get_random_pokemon()

# Récupère le nombre total de Pokémon.
@app.get("/pokemons/count", response_model=dict)
def get_pokemon_count():
    return fonction.get_pokemon_count()

# Récupère les Pokémon les plus forts.
@app.get("/pokemons/strongest", response_model=List[Pokemon])
def get_strongest_pokemons(top: int = 10):
    return fonction.get_strongest_pokemons(top)

# Récupère les Pokémon les plus faibles.
@app.get("/pokemons/weakest", response_model=List[Pokemon])
def get_weakest_pokemons(top: int = 10):
    return fonction.get_weakest_pokemons(top)

# Récupère la chaîne d'évolution d'un Pokémon.
@app.get("/pokemons/evolution-chain/{pokemon_id}", response_model=List[Pokemon])
def get_evolution_chain(pokemon_id: int):
    return fonction.get_evolution_chain(pokemon_id)

# Récupère les Pokémon par mouvement.
@app.get("/pokemons/move/{move_name}", response_model=List[Pokemon])
def get_pokemon_by_move(move_name: str):
    return fonction.get_pokemon_by_move(move_name)

# Recherche les Pokémon par type avec une liste de types.
@app.get("/pokemons/search/", response_model=list)
async def search_pokemon_by_type(types: str = Query(..., title="Type(s) of Pokémon")):
    type_list = types.split(",")
    return fonction.search_pokemon_by_type(type_list)

# Filtre les Pokémon par statistiques.
@app.get("/pokemons/filter/", response_model=list)
async def filter_pokemon_by_stats(min_hp: int = None, max_hp: int = None,
                                  min_attack: int = None, max_attack: int = None,
                                  min_defense: int = None, max_defense: int = None,
                                  min_sp_attack: int = None, max_sp_attack: int = None,
                                  min_sp_defense: int = None, max_sp_defense: int = None,
                                  min_speed: int = None, max_speed: int = None,
                                  limit: int = 10):
    return fonction.filter_pokemon_by_stats(min_hp, max_hp,
                                            min_attack, max_attack,
                                            min_defense, max_defense,
                                            min_sp_attack, max_sp_attack,
                                            min_sp_defense, max_sp_defense,
                                            min_speed, max_speed,
                                            limit)

# Recherche les Pokémon par nom.
@app.get("/pokemons/search/name/", response_model=list)
async def search_pokemon_by_name(name: str = Query(..., title="Name of Pokémon")):
   
    return fonction.search_pokemon_by_name(name)

# Récupère les commentaires d'un Pokémon.
@app.get("/pokemons/comments/{pokemon_id}/", response_model=list)
async def get_pokemon_comments(pokemon_id: int):
    return fonction.get_pokemon_comments(pokemon_id)

# Récupère les Pokémon favoris.
@app.get("/pokemons/favorites/", response_model=list)
async def get_favorite_pokemons():
    return fonction.get_favorite_pokemons()

# Met à jour les données d'un Pokémon existant.
@app.put("/pokemons/{pokemon_id}", response_model=dict)
def update_pokemon(pokemon_id: int, pokemon: UpdatePokemon):
    return fonction.update_pokemon(pokemon_id, {k: v for k, v in pokemon.dict().items() if v is not None})

# Supprime un Pokémon de la base de données.
@app.delete("/pokemons/{pokemon_id}", response_model=dict)
def delete_pokemon_endpoint(pokemon_id: int):
    return fonction.delete_pokemon(pokemon_id)

# Supprime un type d'un Pokémon.
@app.delete("/pokemons/{pokemon_id}/types", response_model=dict)
def delete_type_from_pokemon(pokemon_id: int, type: PokemonType):
    return fonction.delete_pokemon_type(pokemon_id, type.type)

# Supprime une capacité d'un Pokémon.
@app.delete("/pokemons/{pokemon_id}/abilities", response_model=dict)
def delete_ability_from_pokemon(pokemon_id: int, ability: PokemonAbility):
    return fonction.delete_pokemon_ability(pokemon_id, ability.ability)


