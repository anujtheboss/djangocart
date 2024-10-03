from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from .models import ShippingAddress,Order,OrderItem
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# create  a orderitem inline
# for adding orderitem to order 
# we can see in the Order model in admin pannel where items are added
class OrderItemInline(admin.StackedInline):
     model=OrderItem
     extra=0
class OrderAdmin(admin.ModelAdmin):
      model=Order
      inlines=[OrderItemInline]
admin.site.unregister(Order)
admin.site.register(Order,OrderAdmin)
