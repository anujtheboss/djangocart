from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UserUpdateForm,UserInfoForm,ChangePasswordForm
from django import forms
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q
from cart.cart import Cart
import json
from .forms import UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def category_summary(request):
    #  fetch categories from category model from database
     categories=Category.objects.all()
     return render(request,'category_summary.html',{'categoreis':categories})
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
            # -------------------------------------------------------------------------------------------------------
                        current_user=Profile.objects.get(user__id=request.user.id)
                        #  get the saved cart from database
                        saved_cart=current_user.old_cart
                        if saved_cart:
                        #    convert to dictionary usign json
                          converted_cart=json.loads(saved_cart)
                        #   add the loaded cart dictionary to our session
                        # get the cart
                          cart=Cart(request)
                          for key,value in converted_cart.items():
                            #    product = Product.objects.get(id=key) 
                            #    cart.add(product=product,quantity=value)
                                # cart.add(product=product)
                        # loop through the cart and add the item from the database
                                cart.db_add(product=key)
                        messages.success(request,('you are successfully logged in'))
                        return redirect('index')
          else:
               messages.success(request,('the password is incorrect'))
               return redirect('index')
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
    


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated! You are able to login')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context ={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'profile.html',context)    
# def update_user(request):
#      if request.user.is_authenticated:
#           current_user=User.objects.get(id=request.user.id)
#           user_form=UpdateUserForm(request.POST or None, instance=current_user)
#           if user_form.is_valid():
#                user_form.save()
#                login(request,current_user)
#                messages.success(request,'user has been updated successfully!!')
#                return redirect('home')
#           return render(request,'update_user.html',{'userform':user_form})
#      else:
#           messages.success(request,'you must be logged in!!')
#           return redirect('index')
     




def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		print(shipping_user)
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('index')
		return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('index')



def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('index')


def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {"categories":categories})	

def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('index')     



def product(request,pk):
     product=Product.objects.get(id=pk)
     return render(request,'product.html',{'products':product})
def search(request):
     if request.method=='POST':
        searched=request.POST['search']
        # searched is the name of input field
        # query the products db model
        searched=Product.objects.filter(name__icontains=searched)
        if not searched:
             messages.success(request,"product doesnot exists!")
             return render(request,'search.html',{})
        else:
             return render(request,'search.html',{'searched':searched})
     else:
        return render(request,'search.html',{})
