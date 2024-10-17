from django.urls import path
from . import views
urlpatterns=[
    path('payment_success',views.payment_success,name="payment_success"),
    path('checkout',views.checkout,name="checkout"),
    path('biling_info',views.biling_info,name='biling_info'),
    path('process_order', views.process_order, name="process_order"),
    path('shipped_dash', views.shipped_dash, name="shipped_dash"),
    path('unshipped_dash', views.not_shipped_dash, name="unshipped_dash"),

]
