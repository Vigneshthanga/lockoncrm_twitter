'''
This file performs the following:

1. Handles the routing between the different pages in the Twitter API app.
2. Utilizes the Twitter API to perform specified Twitter operations according to the business logic
3. Executes the logic for the creation, display, and deletion of the user's Tweets.

Author: Kevin Lai
'''

from flask import Flask, render_template, redirect, url_for
from forms import CreateTweetForm, DeleteTweetForm
import tweepy
import os
from os.path import join, dirname
from dotenv import load_dotenv


app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")

access_token = os.environ.get("ACCESS_KEY")
access_token_secret = os.environ.get("ACCESS_SECRET")
# Put in your own Twitter API keys to authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

twitter_user = api.me()

@app.route("/twitter")
@app.route("/twitter/home/")
def homepage():
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')
    return render_template('home.html')

@app.route("/twitter/create_tweet/", methods=['GET','POST'])
def create_tweet():
	form = CreateTweetForm()
	completion_msg = ""
	if form.validate_on_submit():
		text = form.description.data
		try:
			# Post the tweet
			api.update_status(text)
			completion_msg = "Success! The Tweet has been posted to Twitter."
		except:
			completion_msg = "The Tweet failed to post. Please try again."

	return render_template("create_tweet.html", form = form, completion_msg = completion_msg)

@app.route("/twitter/show_tweet/", methods=['GET','POST'])
def show_tweet():
	user_screen_name = twitter_user.screen_name
	user_tweets = ""
	completion_msg = ""
	tweet_id = ""
	try:
		user_tweets = api.user_timeline()
	except:
		completion_msg = ""
	form = DeleteTweetForm()
	if form.validate_on_submit():
		tweet_id = form.tweet_id.data
		try:
			# Delete a Tweet by typing in its ID
			tweet_id = int(tweet_id)
			api.destroy_status(tweet_id)
			completion_msg = "Success! The Tweet has been deleted."
		except:
			completion_msg = "The value that you entered is not a valid Tweet ID. Please Try Again."
	return render_template("show_tweet.html", form = form, user_screen_name=user_screen_name, tweets=user_tweets, completion_msg = completion_msg)

@app.route("/twitter/about/")
def about_page():
	return "SJSU Fall 2019 CMPE 272 Team Flash"

# The following code is only for testing purposes.
'''
@app.route("/test_create/", methods=['GET','POST'])
def test_create():
	form = CreateTweetForm()
	description_data = form.description.data
	return render_template("create_tweet.html", form = form, d_data = description_data)

@app.route("/twitter/test_show/")
def test_show():
	if failed:
		return redirect(url_for('show_tweet'))
	return render_template("show_tweet.html")
'''

if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.run(debug=True)
