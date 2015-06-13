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
	def get_batch(cls, User, Categories, amount):
		categories = [category.key for category in Categories]
		questions = cls.query(cls.flag_count < 10, cls.category.IN(categories)).fetch(amount)
		# user_answers = Users.get_by_id(User).answered
		# questions = cls.query(cls.flag_count < 10, cls.category in Categories)
		# questions_list = [question for question in questions if User not in answered]
		print questions
		return questions

	def yes_vote(self, User):
		user = Users.get_by_id(User)
		if user.key in self.answered:
			return False
		self.answered.append(user.key)
		self.yes_count = self.yes_count + 1
		self.put()
		return True

	def no_vote(self, User):
		user = Users.get_by_id(User)
		if user.key in self.answered:
			return False
		self.answered.append(user.key)
		self.no_count = self.no_count + 1
		self.put()
		return True


class Categories(BaseModel):
	name = ndb.StringProperty(required = True)




			