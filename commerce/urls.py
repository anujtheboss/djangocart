from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
]
# we created urls for the app and now we need to include this to main urls.py