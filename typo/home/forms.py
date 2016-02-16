from flask_wtf import Form
from wtforms import TextAreaField, IntegerField
import wtforms.validators as v


class CommentForm(Form):
    text = TextAreaField('Текст', validators=[v.required()])
    replyto = IntegerField('Id комментария')