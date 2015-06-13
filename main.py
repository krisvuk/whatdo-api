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

class PostResponse(messages.Message):
	message = messages.StringField(1)

class UserObject(messages.Message):
    email = messages.StringField(1, required = True)
    password = messages.StringField(2)



@endpoints.api(name = 'users', version = 'v1',
               description = 'User Management Resources')
class UsersApi(remote.Service):

    @endpoints.method(UserObject, UserObject,
                        name = 'getUserByEmail',
                        path = 'get_user_by_email',
                        http_method = 'GET')
    def getUser(self, request):
    	user_query = Users.query(Users.email == request.email)
        user = UserObject(email = user_query.email)
        return user

    @endpoints.method(UserObject, PostResponse,
                        name = 'createUser',
                        path = 'create_user',
                        http_method = 'POST')
    def createUser(self, request):
        user_query = Users.query(Users.email == request.email)
        if not user_query.get():
            Users(email = request.email, password = request.password).put()
            post_response = PostResponse(message = "Post successful.")
        else:
            post_response = PostResponse(message = "Error. User with that email already exists.")
        return post_response

@endpoints.api(name = 'questions', version = 'v1',
               description = 'Questions Management Resources')
class Questions(remote.Service):
    pass


application = endpoints.api_server([UsersApi, Questions])

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)