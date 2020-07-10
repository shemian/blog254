from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Update')

class PostForm(FlaskForm):
    title = StringField('Title', validators = [Required()])
    content = TextAreaField('Content', validators = [Required()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = TextAreaField('Content', validators = [Required()])
    submit = SubmitField('Comment')