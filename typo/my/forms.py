from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField
import wtforms.validators as v

from typo.models import Post


class PostForm(Form):
    title = StringField('Заголовок', validators=[v.required('Нужен заголовок')])
    markdown = TextAreaField('Текст', validators=[v.required('Нужен текст')])
    status = SelectField('Статус', choices=Post.STATUS.items())


class ProfileEditForm(Form):
    pass