from google.appengine.ext import ndb

'''
This file contains the database models for WhatDo?
'''

class BaseModel(ndb.Model):
	created = ndb.DateTimeProperty(auto_now_add = True)
	updated = ndb.DateTimeProperty(auto_now = True)

class Users(BaseModel):
	email = ndb.StringProperty(required = True)
	password = ndb.StringProperty(required = True)
	active = ndb.BooleanProperty(default = True)
	favourited = ndb.KeyProperty(repeated = True, kind = "Questions")
	questions = ndb.KeyProperty(repeated = True, kind = "Questions")
	violations = ndb.IntegerProperty(default = 0)


class Questions(BaseModel):
	title = ndb.StringProperty(required = True)
	flag_count = ndb.IntegerProperty(default = 0)
	yes_count = ndb.IntegerProperty(default = 0)
	no_count = ndb.IntegerProperty(default = 0)
	visible = ndb.BooleanProperty(default = True)
	category = ndb.KeyProperty(kind = "Categories")
	answered = ndb.KeyProperty(repeated = True, kind = "Users")
		
	@classmethod
	def get_batch(cls, User, Categories):
		print User
		print [category.key for category in Categories]
		# questions = cls.query(cls.flag_count < 10, cls.category in Categories)
		# questions_list = [question for question in questions if User not in answered]
		# return questions_list


class Categories(BaseModel):
	name = ndb.StringProperty(required = True)




			