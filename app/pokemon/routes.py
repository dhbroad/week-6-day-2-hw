from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import requests as r

pokemon = Blueprint('pokemon', __name__, template_folder="pokemon_templates")

from .forms import AddPokemonForm
from app.models import db, Pokemon


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
            if count == 1:
                ability1 = item['ability']['name']
            elif count == 2:
                ability2 = item['ability']['name']
            my_abilities.append((item['ability']['name']))
            count += 1
        my_img = my_data['sprites']['front_default']
        pokemon = Pokemon(name, my_img, ability1, ability2)
        return render_template('pokemon.html', abilities=my_abilities, img_url=my_img, name=name, pokemon = pokemon)
    return redirect(url_for('home'))


# @pokemon.route('/pokemon/add/<int:pokemon_id>')
# def addToPokedex(pokemon_id):
#     form = AddPokemonForm()
#     if request.method == "POST":
#         if form.validate():
#             pokemon_name = form.pokemon_name.data
#             img_url = form.img_url.data
#             ability1 = form.ability1.data
#             ability2 = form.ability2.data

#             pokemon = Pokemon(pokemon_name, img_url, ability1, ability2)

#             db.session.add(pokemon)
#             db.session.commit()  
#     return redirect(url_for('home'))

@pokemon.route('/pokemon/add')
@login_required
def addToPokedex(name):
    name = request.form.to_dict()['name']
    data = r.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    my_data = data.json()
    abilities = my_data['abilities']
    my_abilities = []
    count = 1
    for item in abilities:
        if count == 1:
            ability1 = item['ability']['name']
        elif count == 2:
            ability2 = item['ability']['name']
        my_abilities.append((item['ability']['name']))
        count += 1
    my_img = my_data['sprites']['front_default']
    pokemon = Pokemon(name, my_img, ability1, ability2)
    db.session.add(pokemon)
    db.session.commit()
    return redirect(url_for('home'))