from django.db import models
from model_utils import Choices

# class for category of the course, each course belongs to some category
class CategoryOfCourse(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return str(self.id) + '  ' + self.name


# class for tags, each course have (0,1,2,...) tags
class TagOfCourse(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + '  ' + self.name


# class for levels , each course can be Easy, Medium or Hard
class LevelOfCourse(models.Model):
    level = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + '  ' + self.level


# class for courses, each course has name, length (how many minutes it lasts),
# level (Easy,Medium,Hard) - FK , category - FK, tags - ManyToMany
class CourseOfApp(models.Model):
    name = models.CharField(max_length=60)
    length = models.IntegerField()
    # LEVEL = Choices('poczatkujacy','srednio_zaawansowany','zaawansowany')
    # level=models.CharField(choices=LEVEL,default=LEVEL.poczatkujacy,max_length=30)
    level = models.ForeignKey(LevelOfCourse, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryOfCourse, on_delete=models.CASCADE)
    tags = models.ManyToManyField(TagOfCourse, null=True, blank=True)

    def __str__(self):
        return str(self.id) + ' ' + self.name


# class for users, each user has name, surname, nickname (Unique), and also courses(0,1,2...) - ManytoMany
class UserOfApp(models.Model):
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)
    nickname = models.CharField(unique=True, max_length=60)
    courses = models.ManyToManyField(CourseOfApp, null=True, blank=True)

    def __str__(self):
        return self.nickname


# bridge class(table) between users and their courses, each ProgressInCourse object describes actualTime,
# which is actual time spent on a course by user
class ProgressInCourse(models.Model):
    person = models.ForeignKey(UserOfApp, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseOfApp, on_delete=models.CASCADE)
    actualTime = models.IntegerField()

    def __str__(self):
        return str(self.person) + ' ' + str(self.course)
