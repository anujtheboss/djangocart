# from django.shortcuts import render,get_object_or_404
# from .cart import Cart
# from django.contrib import messages
# from commerce.models import Product
# from django.http import JsonResponse

# # Create your views here.
# def cart_summary(request):
#     cart=Cart(request)
#     cart_products=cart.getproducts()
#     quantities=cart.getquants()
#     totals=cart.totals()
#     return render(request,"cart_summary.html",{"cart_products":cart_products,"quantities":quantities,"totals":totals})
# def cart_add(request):
#        #get the cart
#        cart=Cart(request)
#        print("hello")
#        #test the post
#        if request.POST.get('action')=='post':
#             product_id=int(request.POST.get('product_id'))
#             print(product_id)
#             # receiving product with given id for Product model database
#             product_qty=int(request.POST.get('product_qty'))
#             product=get_object_or_404(Product,id=product_id)
#             # save to session
#             cart.add(product=product,quantity=product_qty)
#             # this calls the add function of cart passing product paramerters
#             #return response
#             # response=JsonResponse({'Product Name :' :product.name})
#             product_qtys=cart.__len__()
#             response=JsonResponse({'qty:' :product_qtys})
#             messages.success(request,("product added to cart!!!"))
#             return response
       
#        pass
# def cart_delete(request):
#       cart=Cart(request)
#       if request.POST.get('action')=="post":
#          product_id=int(request.POST.get('product_id'))
#          cart.delete(product=product_id)
#          response=JsonResponse({'product':product_id})
#          messages.success(request,'item deleted from the cart!!')
#          return response
# def cart_update(request):
#     cart=Cart(request)
#     if request.POST.get('action')=="post":
#          product_id=int(request.POST.get('product_id'))
#          product_qty=int(request.POST.get('product_qty'))
#          cart.update(product=product_id,quantity=product_qty)
#          response=JsonResponse({'qty':product_qty})
#          messages.success(request,'updated sucessfully!!')
#          return response

from django.shortcuts import render, get_object_or_404
from .cart import Cart
from commerce.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.getproducts
	# quantities = cart.getquants
	totals = cart.totals()
	return render(request, "cart_summary.html", {"cart_products":cart_products,"totals":totals})




def cart_add(request):
	# Get the cart
	cart = Cart(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		# product_qty = int(request.POST.get('product_qty'))

		# lookup product in DB
		product = get_object_or_404(Product, id=product_id)
		# Save to session
		# cart.add(product=product, quantity=product_qty)
		cart.add(product=product)
		

		# Get Cart Quantity
		cart_quantity = cart.__len__()

		# Return resonse
		# response = JsonResponse({'Product Name: ': product.name})
		response = JsonResponse({'qty': cart_quantity})
		messages.success(request, ("Product Added To Cart..."))
		return response

	
def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		# Call delete Function in Cart
		cart.delete(product=product_id)

		response = JsonResponse({'product':product_id})
		#return redirect('cart_summary')
		messages.success(request, ("Item Deleted From Shopping Cart..."))
		return response


def cart_update(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		cart.update(product=product_id, quantity=product_qty)

		response = JsonResponse({'qty':product_qty})
		#return redirect('cart_summary')
		messages.success(request, ("Your Cart Has Been Updated..."))
		return response
