from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('api/courses/<levelName>', views.Courses.as_view()),  # get
    path('api/add/course', views.createCourse),  # post
    path('api/<nickname>/courses/<levelName>', views.coursesOfUser.as_view()),  # get
    path('api/connect/<nickname>/<courseid>', views.addCourseToUser),  # post
    path('api/users', views.UsersOfApp.as_view()), #get
    path('api/createuser', views.createUser), #post

]

# LEARN FOR KIVY SORFTWARE
# https://docs.djangoproject.com/en/2.1/topics/db/queries/
# https://docs.djangoproject.com/en/2.1/topics/db/models/
# https://django-filter.readthedocs.io/en/master/
# VIRTUALE
# LINUX
# rest documentation


