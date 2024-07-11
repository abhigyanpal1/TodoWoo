from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def signupuser(request):
      if request.method == 'GET':
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
    
      else:
         if request.POST['password1'] == request.POST['password2']:
           try:
              user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
              user.save()#saves info in the database
              login(request,user)
              return redirect('currenttodos')
           except IntegrityError:
              return render(request,'todo/signupuser.html',{'form':UserCreationForm(), 'error':'Username unavailable, please choose another one'})
         else:
           #leaving this for later printed only because it was showing an indentation error
           return render(request,'todo/signupuser.html',{'form':UserCreationForm(), 'error':'Passwords did not match'})
           #passwords did not match so user ko signup page pe waapis bhej diya aur error message display kar diya

@login_required
def currenttodos(request):
   todos = Todo.objects.filter(user = request.user, dateCompleted__isnull = True )# only show for a particular user and where the dateCompleted is left blank which means that the task has not been completed
   return render(request,'todo/currenttodos.html',{'todos':todos})

@login_required
def completedtodos(request):
   todos = Todo.objects.filter(user = request.user, dateCompleted__isnull = False ).order_by('-dateCompleted')# only show for a particular user and where the dateCompleted is not left blank which means that the task has been completed
   return render(request,'todo/completedtodos.html',{'todos':todos})


def loginuser(request):
   if request.method == 'GET':
      return render(request,'todo/loginuser.html',{'form': AuthenticationForm()})
   else:
      user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
      if user is None:
         return render(request,'todo/loginuser.html',{'form':AuthenticationForm(),'error':'Username and password did not match'})
      else:
         login(request,user)
         return redirect('currenttodos')

@login_required
def logoutuser(request):
   logout(request)
   return redirect("home")

def home(request):
   return render(request,'todo/home.html')

@login_required
def createtodo(request):
   if request.method == 'GET':
      return render(request, 'todo/createtodo.html', {'form':TodoForm()})
   else:
      try:
         form = TodoForm(request.POST)
         newtodo = form.save(commit = False)
         newtodo.user = request.user
         newtodo.save()
         return redirect('currenttodos')
      except ValueError:
         return render(request,'todo/createtodo.html',{'form':TodoForm(),'error':'Bad data passed in. Try again!'})

@login_required      
def viewtodo(request, todo_pk): #user = request.user makes sure that koi aur user kisi aur ka todo update ya dekh na paye
   todo = get_object_or_404(Todo,pk = todo_pk, user = request.user)# Todo is the class and pk is primary key
   if request.method == "GET": # agar request method get hua tabhi form show hona chahiye
     form = TodoForm(instance = todo)# takes the already existing data from the admin jo ki humnein mangaya tha and fills those details in a form
     return render(request,'todo/viewtodo.html',{'todo':todo,'form':form})
   else:
      try:# instance = todo tells that it is an existing object that we are trying to update
         form = TodoForm(request.POST, instance = todo) # data submitted via the form is stored in the form object
         form.save()
         return redirect('currenttodos')
      except ValueError:
         return render(request,'todo/viewtodo.html',{'todo':todo,'form':form, 'error':'Bad data passed in. Please try again!'})

@login_required
def completetodo(request, todo_pk):
   todo = get_object_or_404(Todo,pk = todo_pk, user = request.user)
   if request.method == "POST":
      todo.dateCompleted = timezone.now()# sets the dateCompleted to the current date and hence this element is not null anymore because of which this todo object will be removed from currenttodos
      todo.save()
      return redirect('currenttodos')

@login_required        
def deletetodo(request, todo_pk):
   todo = get_object_or_404(Todo,pk = todo_pk,user = request.user)
   if request.method == "POST":
      todo.delete()
      return redirect('currenttodos')



