from django.forms import ModelForm
from .models import Todo

class TodoForm(ModelForm):
    class Meta:
        model = Todo # specifies which model we are using 
        fields = ['title','memo','important'] # which fields we want to show on our form