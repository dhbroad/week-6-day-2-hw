from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import requests as r

pokemon = Blueprint('pokemon', __name__, template_folder="pokemon_templates")


from app.models import db, Pokemon, Pokedex
from .forms import CreatePokemonForm



@pokemon.route('/pokemon', methods=["POST"])
def myPokemon():
    name = request.form.to_dict()['name']
    data = r.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if data.status_code == 200:
        my_data = data.json()
        abilities = my_data['abilities']
        my_abilities = []
        count = 1
        for item in abilities:
            print(item['ability']['name'])
            my_abilities.append((item['ability']['name']))
            if count == 1:
                print(f"{item['ability']['name']} should be ability1")
                ability1 = item['ability']['name']
                print(f"{ability1} has been assigned to ability1")
            elif count == 2:
                print(f"{item['ability']['name']} should be ability2")
                ability2 = item['ability']['name']
                print(f"{ability2} has been assigned to ability2")
            count += 1
        my_img = my_data['sprites']['front_default']
        pokemon = Pokemon.query.filter_by(pokemon_name=name).first()
        if pokemon is None:
            pokemon = Pokemon(name, my_img, ability1, ability2)
            db.session.add(pokemon)
            db.session.commit()
        return render_template('pokemon.html', abilities=my_abilities, img_url=my_img, name=name, pokemon=pokemon)
    return redirect(url_for('home'))


# POKEDEX FUNCTIONALITY
@pokemon.route('/pokedex')
@login_required
def showPokedex():
    pokedex = Pokedex.query.filter_by(user_id=current_user.id)
    count = {}
    for apokemon in pokedex:
        count[apokemon.pokemon_id] = count.get(apokemon.pokemon_id, 0) + 1
    
    pokedex_pokemon = []
    for pokemon_id in count:
        pokemon_info = Pokemon.query.filter_by(id=pokemon_id).first().to_dict()
        pokedex_pokemon.append(pokemon_info)

    return render_template('pokedex.html', pokedex = pokedex_pokemon)


@pokemon.route('/pokedex/add/<int:pokemon_id>') # for adding from a list of pokemon
def addToPokedex(pokemon_id):
    pokedex_pokemon = Pokedex(current_user.id, pokemon_id)
    pokedex = Pokedex.query.filter_by(pokemon_id=pokemon_id).first()
    if pokedex is None:
        db.session.add(pokedex_pokemon)
        db.session.commit()
        print(f"Pokemon added to Pokedex successfully!")
        return redirect(url_for('home'))
    else: 
        print(f"That Pokemon was already in your Pokedex!")
        return redirect(url_for('home'))

