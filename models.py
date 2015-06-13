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