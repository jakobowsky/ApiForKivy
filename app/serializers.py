from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CategoryOfCourse
        fields = ('id', 'name')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TagOfCourse
        fields = ('id', 'name')


class LevelOfCourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LevelOfCourse
        fields = ('id', 'level')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    level = LevelOfCourseSerializer()

    class Meta:
        model = CourseOfApp
        fields = ('id', 'name', 'length', 'level', 'category', 'tags')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    courses = CourseSerializer(many=True)
    class Meta:
        model = UserOfApp
        fields = ('id', 'name', 'surname', 'nickname', 'courses')



class ProgressSerializer(serializers.HyperlinkedModelSerializer):
    course = CourseSerializer()
    userOfCourse = UserSerializer()

    class Meta:
        model = ProgressInCourse
        fields = ('id', 'actualTime', 'person', 'course')
