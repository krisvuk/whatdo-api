import webapp2
from models import *

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('The application is working with no bugs.')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
