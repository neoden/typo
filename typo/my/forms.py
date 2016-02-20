from flask_wtf import Form
from wtforms import TextField, TextAreaField, BooleanField
from wtforms.fields.html5 import EmailField
import wtforms.validators as v


class PostForm(Form):
    title = TextField('Заголовок', validators=[v.required()])
    text = TextAreaField('Текст', validators=[v.required()])
    publish = BooleanField('Опубликовать')


class ProfileEditForm(Form):
    pass