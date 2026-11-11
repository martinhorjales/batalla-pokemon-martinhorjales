from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class EntrenadorForm(FlaskForm):
    trainer = StringField(
        'Nombre del Entrenador', 
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=15, message="El nombre debe tener entre 3 y 15 caracteres.")
        ]
    )
    submit = SubmitField('Comenzar Aventura')