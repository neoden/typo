from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField
import wtforms.validators as v


class PostForm(Form):
    title = StringField('Заголовок', validators=[v.required()])
    markdown = TextAreaField('Текст', validators=[v.required()])
    publish = BooleanField('Опубликовать')


class ProfileEditForm(Form):
    pass