from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddPokemonForm(FlaskForm):
    pokemon_name = StringField('Title', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    ability1 = StringField('Ability1', validators=[])
    ability2 = StringField('Ability2', validators=[])
    submit = SubmitField()