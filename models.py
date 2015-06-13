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

class Questions(BaseModel):
	title = ndb.StringProperty(required = True)
	flag_count = ndb.IntegerProperty(default = 0)
	yes_count = ndb.IntegerProperty(default = 0)
	no_count = ndb.IntegerProperty(default = 0)
	visible = ndb.BooleanProperty(default = True)
	
	def check_flag_count(self):
		if (self.flag_count > 10):
			self.visible = False
	
	@classmethod
	def get_batch(self):
		if (self.check_flag_count = True)


class Categories(BaseModel):
	name = ndb.StringProperty(required = True)

class UsersToQuestions(BaseModel):
	user = ndb.KeyProperty(default = True)
	question = ndb.KeyProperty(default = True)

class UsersToCategories(BaseModel):
	user = ndb.KeyProperty(default = True)
	category = ndb.KeyProperty(default = True)

class QuestionsToCategories(BaseModel):
	question = ndb.KeyProperty(default = True)
	category = ndb.KeyProperty(default = True)

class UsersFlaggedCount(BaseModel):
	user = ndb.KeyProperty(default = True)
	flag_count = ndb.IntegerProperty(default = 0)


			