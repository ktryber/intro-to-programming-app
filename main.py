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
import cgi
import validation


from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime

from os import path


import jinja2
import webapp2



JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))



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

		
		greeting.content = self.request.get('content')
		greeting.put()
		query_params = {'guestbook_name': guestbook_name}
		self.redirect('/?' + urllib.urlencode(query_params))
		




################# Pages ##################
class MainPage(Handler):
	def get(self):
		title = "Kris Tryber Intro to Programming"
		login = users.create_login_url(self.request.uri)
		logout = users.create_logout_url(self.request.uri)
		user = users.get_current_user()
	
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		posts_to_fetch = 10
		greetings_query = Greeting.query(ancestor=guestbook_key(DEFAULT_GUESTBOOK_NAME)).order(-Greeting.date)
		greetings = greetings_query.fetch(posts_to_fetch)
		

		self.render("base.html", title=title, user=user, login=login, logout=logout, greetings=greetings,)

class Invalid(Handler):
	def get(self):
		title = "Kris Tryber Intro to Programming Stage 1"
		user = users.get_current_user()
		login = users.create_login_url(self.request.uri)
		logout = users.create_logout_url(self.request.uri)


class Stage1(Handler):
	def get(self):
		title = "Kris Tryber Intro to Programming Stage 1"
		user = users.get_current_user()
		login = users.create_login_url(self.request.uri)
		logout = users.create_logout_url(self.request.uri)

		

		#comments stage 1
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		posts_to_fetch = 10
		greetings_query = Greeting.query(ancestor=guestbook_key(DEFAULT_GUESTBOOK_NAME)).order(-Greeting.date)
		greetings = greetings_query.fetch(posts_to_fetch)

		


		
		concepts_1_1 = [ 

		["11", "HTML Notes", "Browsers are built to read pages of HTML code that then display text. HTML is written with a series of elements and tags that are organized in tree like structures from biggest to smallest. CSS then comes in to make that content have color, borders, flexible structure so that web pages can be viewed on different screen sizes, etc." ]
		]
		 
		concepts_1_2 = [

		["21", "In-line vs. Block Elements", "HTML elements can either be in-line or block.<h3>In-line</h3><p>Elements that appear in-line with the text and do not have an invisible box around them.</p><ul><li>span</li><li>a</li><li>img</li></ul><h3>Block</h3><p>Elements that have invisible boxes around them, most important for taking a mock up from a pdf format to HTML.</p><ul><li>h1,h2,h3</li><li>p</li><li>div</li></ul>"],

		["22", "Text Editor", "I'm using Sublime Text, I've used it while learning PHP and Wordpress."],

		["23", "HTML Structure", "HTML code is written in a tree like structure to provide easier code readability. The indentation within the code presents to code in a readable fashion and allows you to stay organized when you have multiple elements working together."],

		["24", "Box Model", "<p>The Box model:<br><span class=""margin-color"">Margin</span> - Surrounds the box and serves as the space between the boxes<br><span class=""border-color"">Border</span> - Borders the padding and the content<br><span class=""padding-color"">Padding</span> - The padding clears the area around the content and takes the background color of the box, protects the content in the box.<br><span class=""content-color"">Content</span> - This is the image or the text or the center of the box model.<br> </p><div class=""outer-box""><div id=""box-model"" class=""box"">Content...   </div></div>"],

		["25", "Box Sizing Techniques", "<ol><li>Set box sizes in percentages rather than pixels so that it changes with the browser size.</li><li>Set the box-sizing attribute to border-box for every element. see the CSS for the code.</li><li>Boxes are block style elements so before adjusting they will always take the whole width of the page. adding the display:flex; code to the surrounding div will allow them to appear next to each other.</li></ol>"],

		["26", "Code, Test, Refine", "<ol><li>Look for natural boxes</li><li>Look for repeated styles and semantic elements</li><li>Write your HTML</li><li>Apply styles from biggest to smallest</li><li>Fix things</li></ol>"],

		["27", "Looking for errors in HTML and CSS", "<ul><li><a href=""http://validator.w3.org/#validate_by_input"">To verify HTML</a></li><li><a href=""http://jigsaw.w3.org/css-validator/#validate_by_input"">To verify CSS</a></li></ul>" ]

		]


		self.render("stage1.html", title=title, user=user, concepts_1_1=concepts_1_1, concepts_1_2=concepts_1_2, login=login, logout=logout, greetings=greetings)


class Stage2(Handler):
	def get(self):
		title = "Kris Tryber Intro to Programming Stage 2"
		user = users.get_current_user()
		login = users.create_login_url(self.request.uri)
		logout = users.create_logout_url(self.request.uri)

		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		posts_to_fetch = 10
		greetings_query = Greeting.query(ancestor=guestbook_key(DEFAULT_GUESTBOOK_NAME)).order(-Greeting.date)
		greetings = greetings_query.fetch(posts_to_fetch)

		concepts_2_1 = [

		["Notes Link", "<a href=""https://www.evernote.com/shard/s250/nl/32113319/ebce4900-4c30-46bb-a628-6d7a8801125a/"">Stage 2 Lesson 1:Evernote Notes</a>"],

		["Programming Intro", "The programs you'll write in this class will be Python code. Those will be input to another program which is a Python interpreter that follows the instructions in your code and it does that by following the instruction in its code... and you'll be able to run all that using your web browser.<ul><li>Computers need programs to tell them what to do.</li><li>The computer will need a very precise sequence of steps to tell it how to behave.</li><li>Python is an interpreter that takes our code and tells the computer how to react.</li><li>We have to use exact grammar and everything must be spelled perfectly for the code to actually figure out what we want it to do. It cannot guess like a human would based on the information given.</li></ul>"],

		["Python Grammar", "Examples:Python grammar to arithmetic expressions<br>Expression > Expression Operator Expression<br>Expression > Number<br> Operator > +<br>Operator > *<br>Number > 0,1...<br>Expression > (Expression)<br><br>example:<br> Expression<br>Expression Operator Expression<br>Number + Number<br>1 + 1<br><br>Expression<br> Expression Operator Expression<br>Expr Opr Expr + Number<br>Number * Expr Opr Expr<br>2 * 1+1<br>" ]

		]

		concepts_2_2 = [

		["Notes Link", "<a href=""https://www.evernote.com/shard/s250/nl/32113319/f23bfc48-77a7-4a9f-8ce5-16949690d093/"">Stage 2 Lesson 2:Evernote Notes</a>"],

		["Variable Assignment", "<ul><li>To introduce a variable to python you need to use an ""Assignment Statement"".</li><li>Variable names can only have letters, numbers and underscores and must begin with an underscore or letter.</li></ul><p>example: name = expression<br>speed_of_light = 299792458<br>billionth = 1.0 / 1000000000<br></p><ul><li>= means assignment, think of it as an arrow.</li><li>When you use the same variable name later in Python code with a different value the old variable will still exist but it will be overwritten with the new variable value.</li></ul>"],

		["Strings", "A sequence of characters surrounded by single quotes or double quotes. You can 'start the string' in single quotes and ""end the string"" in double quotes.  If a string starts with a single quote it must end in a single quote and vice vera.<br>ex:<br>print 'Hello'<br>print ""Hello"""],

		["Concatenation", "Close your strings and put a space and plus symbol between them.<br>ex:<br>'Hello'"" + "'!'"" " = " "Hello!"""],

		["Indexing Strings", "string[expression]<br>ex:<br>'udacity'[1+1] -- 'a'<br><br>name = 'kris'<br>print name[0] -- 'k'"], 

		["Selecting Sub-Sequences", "string[expression>:expression]<br>s         number        number <br><br>- String that is a subsequence of the characters in s starting from position start and ending with position stop<br>ex:<br>word = 'assume'<br>print word[3] prints u<br>print word[3:4] prints u<br>print word[4:6] prints me<br>print word[4:] prints me<br>print word[:2] prints as<br>print word[:] prints assume<br><br>-If you want to add something to your selection like an uppercase ""A"" instead of a lower case a like in our variable ""word"" you would need to select ""ssume"" and concatenate it with ""A"". ex:<br><br>ex:<br>print 'A' + word[1:]"],

		["Finding Strings in Strings", "Find is a method in Python.<br>string.find(string) = number that gives first position in search string where the target string appears. If the target is not found it will output -1.<br><br>"],

		["Adding Parameters to Find", "string.find(string,number) = If there are multiple occurrences of your find you can decide where to start the results of your find with a number parameter."],

		]

		concepts_2_3 = [

		["Notes Link", "<a href=""https://www.evernote.com/shard/s250/nl/32113319/1b77d660-998b-4538-b5c9-297f4865dc14/"">Stage 2 Lesson 3:Evernote Notes</a>"],

		["Functions and Procedures", "- def = Define<br>- Using Procedures:<br>procedure(input, input, input)<br>return output<br><br>ex:<br>def sum3(c, d, e):<br>return c + d + e<br><br>print sum3(1,2,3)<br>print sum3(93,53,70)<br>"],
										
		]

		concepts_2_4 = [

		["Equality Comparisons", "Equalities in Python produce a true or false (boo lean) result. You can use less than, Greater than, less than or equal to, greater than or equal to and is not equal to (!=).<br><br>Double equal is ""equal to""."],

		["if", "If allows you to write code that executes equality statements."], 

		["else", "Else statements will run when the if statement is not true.  Is 1 greater than 2, if yes true else false."],

		["While", "While loops allow us to execute a test expression within a procedure over and over again until as long as it is true, when it becomes false it will stop and continue to the next piece of code.<br><br>Break: Allows a while loop to stop even if it is true so you can get out of the loop and execute the following code."],

		]

		concepts_2_5 = [

		["Notes Link", "<a href=""https://www.evernote.com/l/APphiRXQFChEeJVHvnLyy1P0w18cfmMmFYw"">Stage 2 Lesson 5: Evernote Notes</a>"],

		["String vs. List", "A string is a sequence of characters and a list can be a sequence of anything. you can access things in a list by indexing similar to how you would index a string."],

		["Mutation", "Allows you to change the value of the elements inside a list after it has been created."],

		["Aliasing", "Having two different ways to refer to the same object in programming. If you have two variables that refer to the same object it will change the value for both variables."],

		["Append", "A method that adds a new element to the end of a list. It mutates an existing list instead of creating a new list to add the new element."],

		["len()", "Short for length, pass in an object that you want to know the length for."],

		["Index", "Index can be used to produce the position of an element within a list. If it's true it will  return the position if it's false it will produce an error. In lesson 5 we used index with an if statement thus allowing us to produce an else without error.<br><br>if t in p:return p.index(t)else:return -1"],

		["Add AND Assignment Operator", "Adds the right operand to the left operand and assigns the result to the left operand. c += is equivalent to c = c + a"]
		]



		self.render("stage2.html", greetings=greetings, title=title, user=user, concepts_2_1= concepts_2_1, concepts_2_2=concepts_2_2, concepts_2_3=concepts_2_3, concepts_2_4=concepts_2_4, concepts_2_5=concepts_2_5, login=login, logout=logout)

class Stage3(Handler):
	def get(self):
		title = "Kris Tryber Intro to Programming Stage 3"
		user = users.get_current_user()
		login = users.create_login_url(self.request.uri)
		logout = users.create_logout_url(self.request.uri)

		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		posts_to_fetch = 10
		greetings_query = Greeting.query(ancestor=guestbook_key(DEFAULT_GUESTBOOK_NAME)).order(-Greeting.date)
		greetings = greetings_query.fetch(posts_to_fetch)

		concepts_3_toc = ["<ul><li><a href=""#vocabulary"">Vocabulary</a></li><li><a href=""#process"">Movie Website Process</a></li><li><a href=""#summary"">Summary</a></li></ul>"],

		concepts_3_vocab = [

		["Class", "A way to tell Python to create a new type of ""thing"". A class can also be compared to a blueprint that can hold data and methods.  We then use that blueprint to create new things.  Classes are very important to object oriented programming because it allows us to re use code.<br>ex: We created a media.py file that contained the class Movie that took instance variables like movie title, storyline, the poster image and the youtube trailer. Once created we could then create as many instances of class movie re using the same code every time."],

		["Object", "Two meanings: the most basic type of ""thing"", and any instance of some thing."],

		["Instance", "When you use your created classes for something. <br> ex: toy_story and our other movies are an instance of the class Movie.  We reused our class movie over and over to add each movie to our movies web page."],

		["Self", "Inside the functions in a class, self is a convention for the instance/object being accessed. You could use any other word in place of self but since it is widely used it will make your code more readable.  "],

		["inheritance", "The concept that one class can inherit traits from another class, Much like you and your parents. Designing code using inheritance allows you to reuse already written code to add  and amend throughout your program.<br><br> How to use: When you want one class to inherit variables from another class add the inherited class name as an argument in the new class.  ex: class Child(Parent):<br><br>Doing this allows you to access the class and instance variables in the original class inside your new class. Within our inheritance.py file we had a class named parent that took last_name and eye_color as instance variables, then when we created class Child pulling those class and instance variables in, reusing the code and then adding another instance variable for number of toys.<br><br><img src=""/screenshots/inheritance.png"" alt=""inheritance"">"],

		["Constant Variable", "When defining a constant variable the Google python style guide calls for it to be named in all caps.  These are variables that we don't plan on changing or modifying throughout the program. For example, we had movie ratings in our movies web page as a constant variable because those would never change.	"],

		["Class Variable", "Variables attached to classes. These are for attributes and methods that will be shared by all instances of the class. ex: our VALID_RATINGS variable will be shared by every instance created from class Movie.<br><br><img src=""/screenshots/ClassVariable.png"" alt=""Class Variable Example"">"],

		["Definition Screenshot", "<img src=""/screenshots/ClassDefinitions.png"" alt=""Python Class Definitions"">"],

		["Module", "A source file within your python program that you can import into other files to use things like classes that are built somewhere else. In object oriented program it's good practice to build your classes in one file and then import and pull code as you need it throughout your program to stay organized.<br><br>Within the movies website we had one file (media.py) that held our class Movie which was our blueprint.  Then we had entertainment.py that stored all of the instances of that variable. If we wanted to add more things to the website like tv shows, it would have been a good idea to build those classes in media.py and create another file just for TV shows to keep movies and tv shows separate.<br><br>example: webbrowser is a module within python that we can import so that we can show the movie trailers.<img src=""/screenshots/module.png"" alt=""module example screenshot"">"],

		["Method Overriding", "This is used during inheritance. When you create a new class and you want to pull code from another class without duplication you'll want to create the new class and override the original method. We do this by passing in the original class name as an argument in the new class name and then calling the specific methods in the ancestor class that you want to change or modify. Think of this like a filter.<br><br><img src=""/screenshots/MethodOverride.png"" alt=""Method override example"">"],
		]

		concepts_3_movie = [

		["Step One", "First we created a file named media.py.  This file holds all of our blueprints for the content that we then will create. For now since we only have one type of content (movies) we only have one class or blueprint made. Within this class we have 1 class variable (VALID_RATINGS) then an init constructor with the instance variables that will hold data.<br><br>We also added an instance method show_trailer to open a web browser and show the trailer for each movie.<br><br><img src=""/screenshots/media.png"" alt=""media.py screenshot"">"],

		["Step Two", "Next we created entertainment_center.py. This is where we put all of our content that we want to display (favorite movies). To do this we had to import media.py so that we could access our class Movie (blueprint).  Then we created an instance of class Movie for our favorite movies passing in all the arguments that it requires like title, storyline, cover photo and youtube trailer link. At the bottom of this code we also stored all of our movies into a variable that is then called in another file to start applying these instances to HTML to output on our web page.<br><br><img src=""/screenshots/entertainment_center.png"" alt=""entertainment center screenshot"">"],

		["Step Three", "Then we created fresh_tomatoes.py which included our HTML and CSS. Along with that we created a loop that pulls each movie from entertainment_center.py and places it within the HTML and CSS to make each movie display on the page correctly.<br><br><img src=""/screenshots/fresh_tomato_loop.png"" alt=""Fresh Tomato Loop"">"],

		]

		concepts_3_summary = [

		["Object Oriented Programming", "When writing code in Python copy and pasting code is never a good idea simply because if you ever wanted to change that code you would have to remember every place that you pasted to change the code there as well. Also code will always be changed/altered as the project grows. As your program gets more and more complex creating classes for content that will be duplicated will make it easier to go back and change or edit.<BR><br>A perfect example is my notes website.  If you read the code you can tell that there are 3 pages, one for each stage but all of the HTML is duplicated to create another section or concept.  Each section contains a concept title and content related to the concept.  If I ever wanted to change each section and add an example for each concept I would have to go and edit every concept in this web page.<br><br>What would be better is if I could use python and create a class for a ""concept"" that took arguments for a title and description.<br><br><img src=""/screenshots/classMyContent.png""><br><br>Then once I was done I wanted to go back and add an ""example"" for each concept I could with ease.  The steps to do that would be to add a new member variable for my content class for ""example"".<br><br><img src=""/screenshots/classMyContentExample.png""><br><br>As my notes webpage gets more and more complicated I could keep editing that class to add more items that would be related to each content box. One other thing that I learned from the article linked in my first submission review was the need to keep related functions inside the classes that they are used for to keep the code readable. As the project got bigger this would be a must so that related functions wouldn't get overlooked.  Your classes overtime kind of become a table of contents section of a book. If you go to the code for this class (chapter) it will include all of these things(chapter content or sections).<br><br>In stage 2 we learned how to do this with functions but it used lists and indexing to find which content to put where. If we were to rewrite that into a class it would be much cleaner.<br><br>HTML/CSS classes and Python classes work in a similar way which is a good example of how a class works. Each CSS class on this web page is a blueprint so that I can re use the class over and over again to get the same result without copy and pasting.  I then could go change anything about that blueprint in my intro.css and it would change throughout the whole website eliminating the possibly of error.<br><br>The other way to do this would be to go through and add in-line CSS to each section but then if I ever needed to change the font color or size I would have to do it for every instance. In summary intro.CSS is a file that contains multiple blueprints for various sections that I have setup and whenever I need to create another section I just pull from those blueprints to create new instances of the CSS classes or id's.<br><br>This is a good example of Object Oriented Programming in HTML because if anyone was to read the code or wanted to make a change to the ""concept_title"", they could find that in my intro.css folder and make the change without causing any errors."]
		]

		self.render("stage3.html", greetings=greetings, title=title, user=user, concepts_3_toc=concepts_3_toc, concepts_3_vocab=concepts_3_vocab, concepts_3_movie=concepts_3_movie, concepts_3_summary=concepts_3_summary,login=login, logout=logout)

class Stage4(Handler):
	def get(self):
		title = "Kris Tryber Intro to Programming"
		user = users.get_current_user()
		login = users.create_login_url(self.request.uri)
		logout = users.create_logout_url(self.request.uri)

		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		posts_to_fetch = 10
		greetings_query = Greeting.query(ancestor=guestbook_key(DEFAULT_GUESTBOOK_NAME)).order(-Greeting.date)
		greetings = greetings_query.fetch(posts_to_fetch)

		concepts_4_1 = [

		["Network Definition", "A network is a group of entities that can communicate, even though they are not directly connected."],

		["Latency","The time it takes a message to get from the source to the destination. Measured in milliseconds (1000ms in a second)."],

		["Bandwidth","Amount of information that can be transmitted per unit.  Million bits per second."],

		["Bit","Smallest unit of information"],

		["Protocols","A set of rules that people agree to that tell you how two people can talk to each other."],

		["HTTP","Hypertext Transfer Protocol"],

		]

		concepts_4_2 = [

		["URL", "Uniform Resource Locater<br><ul><li>HTTP = Protocol</li><lI>www.udacity.com = Host</lI><li>/ = path</li></ul>"],

		["Query Parameters", "Parameters come after the path in a url.  The first parameter is after the question mark in a url and the second and any following are seperated by an ampersand."],

		["URL Fragments", "Fragments are not sent to the server, usually used to access a section of the page."],

		["Status Codes", "<ul><li>200 ok = Found the document</li><li>302 found = document located somewhere else</li><li>404 not found = couldn't find the document</li><li>500 server error</li></ul>"],

		]

		concepts_4_4 = [

		["Dictionaries", "A type in Python just like a string or a list. Dictionaries are created with a name like a variable and curly brackets.  Each item will have a key and a value.<br><br>dictionary = {'h':1, 'b': 2, 'c':3}"],

		]
		
		concepts_4_5 = [

		["GET vs. POST", "Post:<ul><li>Parameters in the request body</li><li>Used for updating data</li><li>not ok to cache</li><li>Ok to change the server</li></ul><br>Get:<ul><li>Parameters in the URL</li><li>Used for fetching documents</li><li>Ok to cache</li><li>Max URL length(2k characters)</li></ul>"],

		]

		concepts_4_6 = [

		["Validation", "We always want to verify on the server side that we receive what we expected to receive.<br><br>When you have forms or user inputs on your website or app, we need to limit what the user can enter so that they don't have the opportunity to enter malicious content into our forms. We can do that by adding things like drop downs or data validation into our code."],

		["Validation Example", "In our Birthday form that we made during lesson 4 we created a separate file strictly for validation that we then pulled into our main python file that generated the form.<br><br><img src=""/screenshots/lesson4validation.png""><br><br>Then we pulled that file in by importing it. <br><br><img src=""/screenshots/validationimport.png""><br><br>We can then use our code within our form_validation file.  In this case we built validation for the month, day and year. To validate first we requested the content, then created variables using our validation functions.<br><br><img src=""/screenshots/validatingMonthDayYear.png"">""<br><br>This is important because forms on websites can targets for hacking and malicious content. So whenever we install a form we want to make sure that the user is only allowed to input what we have intended for them to input."],

		]

		concepts_4_8 = [

		["Database", "A program that stores, structures and retrieves data."],

		["Database Transactions: ACID", "Atomicity: All parts of a transaction succeed or fail together.<br>Consistency: The database will always be consistent.<br>Isolation: No transaction can interfere with another<br>Durability: Once the transaction is committed, it wont be lost."]

		]
		self.render("stage4.html", greetings=greetings, title=title, user=user, login=login, logout=logout, concepts_4_1=concepts_4_1, concepts_4_2=concepts_4_2, concepts_4_4=concepts_4_4, concepts_4_5=concepts_4_5, concepts_4_6=concepts_4_6, concepts_4_8=concepts_4_8)


app = webapp2.WSGIApplication([

('/', MainPage),
('/stage1', Stage1),
('/stage2', Stage2),
('/stage3', Stage3),
('/stage4', Stage4),
('/sign', Guestbook),
('/invalid', Invalid) 
], debug=True)


