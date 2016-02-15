from flask_wtf import Form
from wtforms import TextAreaField
import wtforms.validators as v


class CommentForm(Form):
    text = TextAreaField('Текст', validators=[v.required()])
