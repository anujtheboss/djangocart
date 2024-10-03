from django.shortcuts import render,redirect
from cart.cart import Cart
# importing Cart class from cart.py
# from .forms import SignUpForm,UpdateUserForm,UserInfoForm,ChangePasswordForm
from django import forms
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress,Order,OrderItem
from django.contrib import messages
from commerce.models import Product
# Create your views here.
def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.getproducts
        quantities = cart.getquants
        totals = cart.totals()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        # Create an Order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            # getting shipping details above from my_shipping and posting those details in order model in database 
            create_order.save()
            # add order items
                # Get the order ID
            order_id = create_order.pk
            
            # Get product Info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()
                                    

            # when checkout the cart must be deleted (lo0p through the sessioin key and delete the session that is saving the information )
            for key in list(request.session.keys()):
                  if key=='session_key':
                        del request.session[key]
            messages.success(request, "Order Placed!")
            return redirect('index')

        else:
            # not logged in
            # Create Order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            # there is full_name in place of user because there is no logged in user
            create_order.save()
            # Add order items
            
            # Get the order ID
            order_id = create_order.pk
            
            # Get product Info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()
            for key in list(request.session.keys()):
                  if key=='session_key':
                        del request.session[key]
            messages.success(request, "Order Placed!")
            return redirect('index')                        
            messages.success(request, "Order Placed!")
            return redirect('index')


    else:
        messages.success(request, "Access Denied")
        return redirect('index')
    

def payment_success(request):
    return render(request,'payment/payment_success.html',{})
def checkout(request):
    cart = Cart(request)
    cart_products = cart.getproducts
    quantities = cart.getquants
    totals = cart.totals()


    if request.user.is_authenticated:
              # checkout as a loggedin user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
        return render(request, "payment/checkout.html", {'cart_products':cart_products,"quantities":quantities ,'shipping_form':shipping_form,"totals":totals})
    else:
        # checkout as a guest user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None)	
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities,"shipping_form":shipping_form,"totals":totals})

def biling_info(request):
    # request.POST has the detail of the previously filled form before submitting
    if request.POST:
        cart = Cart(request)
        cart_products = cart.getproducts
        quantities = cart.getquants
        totals = cart.totals()
        # Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        if request.user.is_authenticated:
            biling_form=PaymentForm ()  
            return render(request,'payment/biling_info.html',{"cart_products":cart_products, "quantities":quantities,"shipping_info":request.POST,"totals":totals,'biling_form':biling_form})
        else:
            biling_form=PaymentForm()
            return render(request,'payment/biling_info.html',{"cart_products":cart_products, "quantities":quantities,"shipping_info":request.POST,"totals":totals,'biling_form':biling_form})
        
        # shipping_form = request.POST
        # return render(request, "payment/biling_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})	
    else:
        messages.success(request,'access denied!')
        return redirect('index')