#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


################# Datastore Keys ############
def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)



################# Datastore Models ############
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)

class Greeting(ndb.Model):
	"""A main model for representing an individual Guestbook entry."""

	author = ndb.StructuredProperty(Author)
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class Notes_db(ndb.Model):
	lesson_number = ndb.IntegerProperty(indexed=True)
	title = ndb.StringProperty(indexed=False)
	content = ndb.StringProperty(indexed=False)
	
############### Handler #################
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

############### Datastore Inputs ############
class Guestbook(webapp2.RequestHandler):
	def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
		guestbook_name = self.request.get('guestbook_name',
                  					DEFAULT_GUESTBOOK_NAME)
		greeting = Greeting(parent=guestbook_key(DEFAULT_GUESTBOOK_NAME))

		if users.get_current_user():
			greeting.author = Author(
				identity=users.get_current_user().user_id(),
				email=users.get_current_user().email())

		content = self.request.get("content").strip()
		comment_error = "whoops, it looks like your comment is invalid"

		if content and not content.isspace():
			greeting.content = content
			greeting.put()
			comment_error = ""
			
		else:
			comment_error

		query_params = {'guestbook_name': guestbook_name, 'comment_error':comment_error}
		self.redirect('/?' + urllib.urlencode(query_params))
		


###### Constant Variables ####

#Number of posts to fetch when displaying the comments
POSTS_TO_FETCH = 10

################# Pages ##################
class MainPage(Handler):
	def get(self):
		title = "Kris Tryber Intro to Programming"
		login = users.create_login_url(self.request.uri)
		logout = users.create_logout_url(self.request.uri)
		user = users.get_current_user()
		comment_error = self.request.get('comment_error')
	
		
	
		greetings_query = Greeting.query(ancestor=guestbook_key(DEFAULT_GUESTBOOK_NAME)).order(-Greeting.date)
		greetings = greetings_query.fetch(POSTS_TO_FETCH)
		

		self.render("base.html", title=title, user=user, login=login, logout=logout, greetings=greetings, comment_error=comment_error)


class Stage1(Handler):
	def get(self):
		title = "Kris Tryber Intro to Programming Stage 1"
		user = users.get_current_user()
		login = users.create_login_url(self.request.uri)
		logout = users.create_logout_url(self.request.uri)
		

		#comments stage 1
		posts_to_fetch = 10
		greetings_query = Greeting.query(ancestor=guestbook_key(DEFAULT_GUESTBOOK_NAME)).order(-Greeting.date)
		greetings = greetings_query.fetch(posts_to_fetch)


		self.render("stage1.html", title=title, user=user, login=login, logout=logout, greetings=greetings)


class Stage2(Handler):
	def get(self):
		title = "Kris Tryber Intro to Programming Stage 2"
		user = users.get_current_user()
		login = users.create_login_url(self.request.uri)
		logout = users.create_logout_url(self.request.uri)

		posts_to_fetch = 10
		greetings_query = Greeting.query(ancestor=guestbook_key(DEFAULT_GUESTBOOK_NAME)).order(-Greeting.date)
		greetings = greetings_query.fetch(posts_to_fetch)


		self.render("stage2.html", greetings=greetings, title=title, user=user, login=login, logout=logout)

class Stage3(Handler):
	def get(self):
		title = "Kris Tryber Intro to Programming Stage 3"
		user = users.get_current_user()
		login = users.create_login_url(self.request.uri)
		logout = users.create_logout_url(self.request.uri)

		posts_to_fetch = 10
		greetings_query = Greeting.query(ancestor=guestbook_key(DEFAULT_GUESTBOOK_NAME)).order(-Greeting.date)
		greetings = greetings_query.fetch(posts_to_fetch)


		self.render("stage3.html", greetings=greetings, title=title, user=user, login=login, logout=logout)

class Stage4(Handler):
	def get(self):
		title = "Kris Tryber Intro to Programming"
		user = users.get_current_user()
		login = users.create_login_url(self.request.uri)
		logout = users.create_logout_url(self.request.uri)

		posts_to_fetch = 10
		greetings_query = Greeting.query(ancestor=guestbook_key(DEFAULT_GUESTBOOK_NAME)).order(-Greeting.date)
		greetings = greetings_query.fetch(posts_to_fetch)


		self.render("stage4.html", greetings=greetings, title=title, user=user, login=login, logout=logout)


app = webapp2.WSGIApplication([

('/', MainPage),
('/stage1', Stage1),
('/stage2', Stage2),
('/stage3', Stage3),
('/stage4', Stage4),
('/sign', Guestbook),
], debug=True)


