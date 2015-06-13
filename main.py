import webapp2

import endpoints
from models import *

from protorpc import messages
from protorpc import message_types
from protorpc import remote


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('The app works')

class GetResponse(messages.Message):
    message = messages.StringField(1)
    success = messages.BooleanField(2)

class PostResponse(messages.Message):
    message = messages.StringField(1)
    success = messages.BooleanField(2)

class UserObject(messages.Message):
    email = messages.StringField(1)
    password = messages.StringField(2)
    message = messages.StringField(3)
    success = messages.BooleanField(4)

class QuestionObject(messages.Message):
    title = messages.StringField(1)
    flag_count = messages.IntegerField(2)
    yes_count = messages.IntegerField(3)
    no_count = messages.IntegerField(4)
    visible = messages.BooleanField(5)
    message = messages.StringField(6)
    success = messages.BooleanField(7)

@endpoints.api(name = 'users', version = 'v1',
               description = 'User Management Resources')
class UsersApi(remote.Service):

    @endpoints.method(UserObject, UserObject,
                        name = 'getUserByEmail',
                        path = 'get_user',
                        http_method = 'GET')
    def getUser(self, request):
        user_query = Users.query(Users.email == request.email).fetch(1)
        if(user_query):
            user = UserObject(email = user_query[0].email, success = True)
        else:
            user = UserObject(message = "Error: could not fetch that user. That user may not exist.", success = False)
        return user

    @endpoints.method(UserObject, PostResponse,
                        name = 'createUser',
                        path = 'create',
                        http_method = 'POST')
    def createUser(self, request):
        user_query = Users.query(Users.email == request.email)
        if not user_query.get():
            Users(email = request.email, password = request.password).put()
            post_response = PostResponse(message = "Post successful.", success = True)
        else:
            post_response = PostResponse(message = "Error. User with that email already exists.", success = False)
        return post_response

@endpoints.api(name = 'questions', version = 'v1',
               description = 'Questions Management Resources')
class Questions(remote.Service):
    pass



@endpoints.api(name = 'categories', version = 'v1',
               description = 'Categories Management Resources')
class Categories(remote.Service):
    pass



application = endpoints.api_server([UsersApi, Questions, Categories])

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)