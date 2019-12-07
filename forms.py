'''
Form UI Class for the Twitter API Operations

Author: Kevin Lai
'''
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class CreateTweetForm(FlaskForm):
	description = TextAreaField('description', validators=[DataRequired(), Length(min = 1, max = 280)])
	create_confirm = SubmitField('Create Tweet')

class DeleteTweetForm(FlaskForm):
	tweet_id = IntegerField('tweet_id', validators=[DataRequired()])
	delete_confirm = SubmitField('Delete Tweet')