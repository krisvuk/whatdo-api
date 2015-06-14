import webapp2

import endpoints
from models import *

from protorpc import messages
from protorpc import message_types
from protorpc import remote


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = Users.query(Users.email == "sandeep@kek.com").fetch(1)[0]
        categories = Categories.query(Categories.name == "Sports").fetch()
        questions = Questions.get_batch(user, categories, 3)
        self.response.write(len(questions))

class GetResponse(messages.Message):
    message = messages.StringField(1)
    success = messages.BooleanField(2)

class PostResponse(messages.Message):
    message = messages.StringField(1)
    success = messages.BooleanField(2)

# category view models
class CategoryObject(messages.Message):
    name = messages.StringField(1)

class CategoryObjects(messages.Message):
    categories = messages.MessageField(CategoryObject, 1, repeated = True)
    list_category_strings = messages.StringField(2, repeated = True)
    user_id = messages.IntegerField(3)

# user view models
class UserObject(messages.Message):
    email = messages.StringField(1)
    password = messages.StringField(2)
    message = messages.StringField(3)
    success = messages.BooleanField(4)

# questions view models
class QuestionObjectCreation(messages.Message):
    title = messages.StringField(1)
    flag_count = messages.IntegerField(2)
    yes_count = messages.IntegerField(3)
    no_count = messages.IntegerField(4)
    visible = messages.BooleanField(5)
    category_id = messages.IntegerField(6)
    answered = messages.MessageField(CategoryObject, 7, repeated = True)
    user_id = messages.IntegerField(8)
    question_id = messages.IntegerField(9)

class QuestionObject(messages.Message):
    title = messages.StringField(1)
    flag_count = messages.IntegerField(2)
    yes_count = messages.IntegerField(3)
    no_count = messages.IntegerField(4)
    visible = messages.BooleanField(5)
    message = messages.StringField(6)
    success = messages.BooleanField(7)
    question_id = messages.IntegerField(8)

class QuestionObjects(messages.Message):
    user_id = messages.IntegerField(1)
    amount = messages.IntegerField(2)
    questions = messages.MessageField(QuestionObject, 3, repeated = True)

@endpoints.api(name = 'users', version = 'v1',
               description = 'User Management Resources')
class UsersApi(remote.Service):

    @endpoints.method(UserObject, UserObject,
                        name = 'get_user',
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
                        name = 'create',
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
class QuestionsApi(remote.Service):

    @endpoints.method(QuestionObjects, QuestionObjects,
                        name = 'get_batch',
                        path = 'get_batch',
                        http_method = 'GET')
    def getBatch(self, request):
        question_objects = []
        user = Users.get_by_id(request.user_id)
        list_of_questions = Questions.get_batch(user, user.categories, request.amount)
        for question in list_of_questions:
            question_objects.append(QuestionObject(title = question.title, yes_count = question.yes_count,
                no_count = question.no_count, flag_count = question.flag_count, visible = question.visible,
                question_id = question.key.id()))
        return QuestionObjects(questions = question_objects)

    @endpoints.method(QuestionObjectCreation, PostResponse,
                        name = 'create',
                        path = 'create',
                        http_method = 'POST')
    def createQuestion(self, request):
        try:
            user = Users.get_by_id(request.user_id)
            category = Categories.get_by_id(request.category_id).key
            question = Questions(title = request.title, category = category).put()
            user.questions.append(question)
            user.put()
            post_response = PostResponse(message = "Post successful. Question created.", success = True)
        except:
            post_response = PostResponse(message = "Error. Question was not created.", success = False)
        return post_response

    @endpoints.method(QuestionObjectCreation, PostResponse,
                        name = 'yes_vote',
                        path = 'yes_vote',
                        http_method = 'POST')
    def yes_vote(self, request):
        question = Questions.get_by_id(request.question_id)
        status = question.yes_vote(request.user_id)
        if status == False:
            post_response = PostResponse(message = "Error. You've already answered this question.", success = False)
        else:
            post_response = PostResponse(message = "Post successful.", success = True)
        return post_response

    @endpoints.method(QuestionObjectCreation, PostResponse,
                        name = 'no_vote',
                        path = 'no_vote',
                        http_method = 'POST')
    def no_vote(self, request):
        question = Questions.get_by_id(request.question_id)
        status = question.no_vote(request.user_id)
        if status == False:
            post_response = PostResponse(message = "Error. You've already answered this question.", success = False)
        else:
            post_response = PostResponse(message = "Post successful.", success = True)
        return post_response

    @endpoints.method(QuestionObjectCreation, PostResponse,
                        name = 'favourite',
                        path = 'favourite',
                        http_method = 'POST')
    def favourite(self, request):
        question = Questions.get_by_id(request.question_id)
        user = Users.get_by_id(request.user_id)
        result = question.favourite(user)
        if result == False:
            post_response = PostResponse(message = "Error.", success = False)
        else:
            post_response = PostResponse(message = "Post successful. Question favourited.", success = True)
        return post_response

    @endpoints.method(QuestionObjectCreation, PostResponse,
                        name = 'unfavourite',
                        path = 'unfavourite',
                        http_method = 'POST')
    def unfavourite(self, request):
        question = Questions.get_by_id(request.question_id)
        user = Users.get_by_id(request.user_id)
        result = question.unfavourite(user)
        if result == False:
            post_response = PostResponse(message = "Error.", success = False)
        else:
            post_response = PostResponse(message = "Post successful. Question unfavourited.", success = True)
        return post_response

    @endpoints.method(QuestionObjectCreation, PostResponse,
                        name = 'flag',
                        path = 'flag',
                        http_method = 'POST')
    def flag(self, request):
        question = Questions.get_by_id(request.question_id)
        result = question.flag(request.user_id)
        if result == False:
            post_response = PostResponse(message = "Error. Question already has answer from user.", success = False)
        else:
            post_response = PostResponse(message = "Post successful. Question flagged.", success = True)
        return post_response


@endpoints.api(name = 'categories', version = 'v1',
               description = 'Categories Management Resources')
class CategoriesApi(remote.Service):

    @endpoints.method(message_types.VoidMessage, CategoryObjects,
                        name = 'get_all',
                        path = 'get_all',
                        http_method = 'GET')
    def getAll(self, request):
        all_categories = []
        categories = Categories.query()
        all_categories = [CategoryObject(name = category.name) for category in categories]
        return CategoryObjects(categories = all_categories)

    @endpoints.method(CategoryObject, PostResponse,
                        name = 'create',
                        path = 'create',
                        http_method = 'POST')
    def createCategory(self, request):
        category_query = Categories.query(Categories.name == request.name)
        if not category_query.get():
            Categories(name = request.name).put()
            post_response = PostResponse(message = "Post successful. Category created.", success = True)
        else:
            post_response = PostResponse(message = "Error. Category with that name already exists.", success = False)
        return post_response

    @endpoints.method(CategoryObject, PostResponse,
                        name = 'create',
                        path = 'create',
                        http_method = 'POST')
    def createCategory(self, request):
        category_query = Categories.query(Categories.name == request.name)
        if not category_query.get():
            Categories(name = request.name).put()
            post_response = PostResponse(message = "Post successful. Category created.", success = True)
        else:
            post_response = PostResponse(message = "Error. Category with that name already exists.", success = False)
        return post_response


    @endpoints.method(CategoryObjects, PostResponse,
                        name = 'addCategoriesToUser',
                        path = 'add_categories_to_user',
                        http_method = 'POST')
    def addCategoriesToUser(self, request):
        categories = Categories.query(Categories.name.IN(request.list_category_strings)).fetch()
        user = Users.get_by_id(request.user_id)
        result = Categories.addCategoriesToUser(user, categories)
        if result == False:
            post_response = PostResponse(message = "Error.", success = False)
        else:
            post_response = PostResponse(message = "Post successful. Categories added.", success = True)
        return post_response

application = endpoints.api_server([UsersApi, QuestionsApi, CategoriesApi])

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)