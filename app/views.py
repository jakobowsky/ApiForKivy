from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
from .serializers import *
from django.http import HttpResponse
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


# class for returning json with courses
# example GET request: 127.0.0.1:8000/api/courses/all or 127.0.0.1:8000/api/courses/Easy <- capital letter matters
class Courses(APIView):
    @method_decorator(csrf_exempt)  # csrf token needed
    def get_courses(self, levelName):  # method which returns courses from selected level
        try:
            levels = [i.level for i in LevelOfCourse.objects.all()]  # selecting all levels from class
            if (str(levelName) == 'all'):  # if we want to get coursed from all levels
                courses = CourseOfApp.objects.all()
                return courses  # returns object of courses

            elif (str(levelName) in levels):  # if we want specified kind of coursed (Easy,Medium,Hard)
                levelObj = LevelOfCourse.objects.get(level=levelName)  # selecting them by levelName
                courses = levelObj.courseofapp_set.all()  # we can get them because of relations between tables
                return courses
        except courses.DoesNotExist:  # handling errors
            raise Http404

    def get(self, request, levelName, format=None):
        courses = self.get_courses(levelName)  # get courses object with selected  level
        # print(courses) #testing
        serializer_context = {
            'request': request,
        }
        serializers = CourseSerializer(courses, many=True, context=serializer_context)
        return Response(serializers.data)  # returning json with our data


# class for returning json with courses of selected user
# example GET request 127.0.0.1:8000/api/<nickname>/courses.<levelName>
# 127.0.0.1:8000/api/adamski912/courses/all or 127.0.0.1:8000/api/jarus122/courses/Easy
class coursesOfUser(APIView):

    def get_courses_of_someone(self, nickname, levelName):
        try:
            man = UserOfApp.objects.get(nickname=nickname)  # get all coursed of selected user (by nickname)
            if levelName == "all":  # if we want all courses
                return man.courses.all()  # we are returing all of them
            else:  # if we want specific courses with specific level
                levelObj = LevelOfCourse.objects.get(level=levelName)  # get level object to filtr coursed
                courses = man.courses.all().filter(level=levelObj)  # get coursed with selected level
                return courses  # returning user's coursed with selected level
        except courses.DoesNotExist:  # handling errors
            raise Http404

    def get(self, request, nickname, levelName, format=None):
        courses = self.get_courses_of_someone(nickname, levelName)

        serializer_context = {
            'request': request,
        }
        serializers = CourseSerializer(courses, many=True, context=serializer_context)
        return Response(serializers.data)  # returning json with selected courses of user


# class which returns json with users who use this webapp
# example GET request  127.0.0.1:8000/api/users
class UsersOfApp(APIView):

    def get_users(self):
        try:
            users = UserOfApp.objects.all()  # query with objects of all users
            return users
        except users.DoesNotExist:  # handlind error
            raise Http404

    def get(self, request, format=None):
        users = self.get_users()
        serializer_context = {
            'request': request,
        }
        serializers = UserSerializer(users, many=True, context=serializer_context)
        return Response(serializers.data)


# Temporary solution, to rewrite as a class base view
# example POST request 127.0.0.1:8000/api/addcourse
# example body of request
# {
#   "name" : "Prolog",
#   "length" : 180,
#   "level" : "2",
#   "category" : "4",
#   "tags" : ["1","2","3"]
# }
# this function create new Course to database
# instead of class base view which has post method, I have coded simple function which handles POST
@api_view(['POST'])
@csrf_exempt
def createCourse(request):
    data = json.loads(request.body.decode("utf-8"))  # instead of serializer, importing json
    tagsIDs = data['tags']  # getting to params from json, here tags
    tagsObj = TagOfCourse.objects.filter(id__in=tagsIDs)  # getting query with all tags objects from json
    categoryObj = CategoryOfCourse.objects.get(id=data['category'])  # query with category object
    levelObj = LevelOfCourse.objects.get(id=data['level'])  # query with level object

    courseObj = CourseOfApp(name=str(data['name']), length=int(data['length']), level=levelObj, category=categoryObj)
    courseObj.save()  # Creating new course object
    courseObj.tags.add(*tagsObj)  # adding tags to it
    courseObj.save()  # save object in database
    return Response({
        'success': True,
    })


# Temporary solution, to rewrite as a class base view
# example POST request 127.0.0.1:8000/api/connect/jarus122/15 <- this adds course with id 15 to jarus122 user
@api_view(['POST'])  # the same as one above this
@csrf_exempt
def addCourseToUser(request, nickname, courseid):  # this adds coures (by id) to user (by nickname)
    userObj = UserOfApp.objects.get(nickname=nickname)
    courseObj = CourseOfApp.objects.get(id=courseid)
    userObj.courses.add(courseObj)
    return Response({
        'success': True,
    })


# create new user with Post request
# example POST 127.0.0.1:8000/api/createuser
# example body of POST request
# {
#    "name" : "Kuba",
#    "surname" : "Sienkiewicz",
#    "nickname" : "sienki22",
#    "courses" :[]
# }
@api_view(['POST'])  # the same as one above this
@csrf_exempt
def createUser(request):  # this adds coures (by id) to user (by nickname)
    data = json.loads(request.body.decode("utf-8"))
    newUser = UserOfApp(name=data['name'], surname=data['surname'], nickname=data['nickname'])
    newUser.save()
    return Response({
        'success': True,
    })


# didn't work solution for a class base view
# class createUser(APIView):
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             print('ok')
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

# class CreateCourse(APIView):
#     print('post req')
#     print('///////////////////////////////////')
#
#     def post(self, request, format=None):
#         serializer = CourseSerializer(data=request.data)
#         if serializer.is_valid():
#             print('ok')
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##############################################################
# index view is used just for testing requests
@api_view(['POST'])
@csrf_exempt
def index(request):
    # print('here')
    # data = json.loads(request.body.decode("utf-8"))  # instead of serializer, importing json
    # tagsIDs = data['tags']  # getting to params from json, here tags
    # tagsObj = TagOfCourse.objects.filter(id__in=tagsIDs)  # getting query with all tags objects from json
    # categoryObj = CategoryOfCourse.objects.get(id=data['category'])  # query with category object
    # levelObj = LevelOfCourse.objects.get(id=data['level'])  # query with level object
    #
    # courseObj = CourseOfApp(name=str(data['name']), length=int(data['length']), level=levelObj, category=categoryObj)
    # courseObj.save()  # Creating new course object
    # courseObj.tags.add(*tagsObj)  # adding tags to it
    # courseObj.save()  # save object in database
    # return Response({
    #     'success': True,
    # })

    # data = json.loads(request.body.decode("utf-8"))
    # print(data['tags'])
    # nickname='jarus122'
    # levelName = 'Easy'
    # man = UserOfApp.objects.get(nickname=nickname)
    # levelObj = LevelOfCourse.objects.get(level=levelName)
    # courses = man.courses.all().filter(level=levelObj)
    # print(courses)

    # level = "Easy"
    # levelObj = LevelOfCourse.objects.get(level=level)
    # print(levelObj)
    # x = LevelOfCourse.objects.all()
    # m = [i.level for i in LevelOfCourse.objects.all()] #names of levels
    # if "Easy" in m:
    #     print ("ok")
    return HttpResponse("TEST")

##################################################################
