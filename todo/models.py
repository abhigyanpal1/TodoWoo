from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length = 100)#specifies the maximum length of a title
    memo = models.TextField(blank = True)#memo(description) about the todo can be left blank
    created = models.DateTimeField(auto_now_add = True)# will be noted as soon as a todo is created
    dateCompleted = models.DateTimeField(null = True, blank = True )
    important = models.BooleanField(default = False)# important checkbox
    user = models.ForeignKey(User, on_delete = models.CASCADE)# way to connect a user and its todos just like in dbms

    def __str__(self):
        return self.title
