from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, BooleanField
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
            FileAllowed(['jpg', 'jpeg', 'png'], 'Only png or jpg images can be uploaded')
        ]
    )
    auto_tags = BooleanField(
        'Autogenerate tags'
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
