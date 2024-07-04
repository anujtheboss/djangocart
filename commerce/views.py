from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
# Create your views here.
def index(request):
#    return  HttpResponse("welcome to my new dango website")
     products=Product.objects.all()
     return render(request,'index.html',{'products':products})
def about(request):
     return render(request,'about.html',{})
def login_user(request):
     if request.method=='POST':
          username=request.POST['username']
          password=request.POST['password']
          user=authenticate(request,username=username,password=password)
          if user is not None:
               login(request,user)
               messages.success(request,('you are successfully logged in'))
               return redirect('index')
          else:
               messages.success(request,('the password is incorrect'))
               return redirect('login')
     else:
          return render(request,'login.html')
    # the password and username would be the superuser that we created before for django admin
def logout_user(request):
     logout(request)
     messages.success(request,('you have been successfully logged out!!'))
     return redirect('index')
def register_user(request):
    form=SignUpForm()
    if request.method=='POST':
         form=SignUpForm(request.POST)
         if form.is_valid():
              form.save()
              username=form.cleaned_data['username']
              password=form.cleaned_data['password1']
              
              user=authenticate(username=username,password=password)
              login(request,user)
              messages.success(request,('successfully registered!'))
              return redirect('index')
         else:
              messages.success(request,("ooops!"))
              return redirect("register")
    else:
         return render(request,'register.html',{'form':form})
        
def product(request,pk):
     product=Product.objects.get(id=pk)
     return render(request,'product.html',{'products':product})
     