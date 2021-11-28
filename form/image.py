from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length
)


class AddImageForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    tags = StringField(
        'Tags'
    )
    image = FileField(
        '',
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png', 'bpm'], 'Only images can be uploaded')
        ]
    )
    submit = SubmitField('Upload')


class EditImageForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    tags = StringField(
        'Tags'
    )
    submit = SubmitField('Upload')
