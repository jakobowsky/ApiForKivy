from django.contrib import admin
from .models import *
admin.site.register(CourseOfApp)
admin.site.register(UserOfApp)
admin.site.register(ProgressInCourse)
admin.site.register(CategoryOfCourse)
admin.site.register(TagOfCourse)
admin.site.register(LevelOfCourse)