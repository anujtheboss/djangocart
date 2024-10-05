# from commerce.models import Product,Profile
# class Cart():
#     def __init__(self,request):
#         self.session=request.session
#         # request can be considered as a user,any time user do any thing in the page they make request
#         self.request=request
#         # get the current session key if it exists
#         cart=self.session.get('session_key')
#         # if the user is new no session key! so create one 
#         if 'session_key' not in request.session:
#              cart=self.session['session_key']={}
    
# # make sure the cart is available on all pages of website
#         self.cart=cart
#     def db_add(self,product,quantity):
#         product_id=str(product.id)
#         product_qty=str(quantity)
#         if product_id in self.cart:
#             # checking if already in cart
#             pass
#         else:
#             # self.cart[product_id]={'price':str(product.price)}
#                  # here product_id is the key of the cart whose value is a dictionary
#             self.cart[product_id]=int(product_qty)

#         self.session.modified=True
#         # dealing with the loggedin user
#         # for persistence of cart in logged out
#         if self.request.user.is_authenticated:
#             # lets gets the current user profile
#             current_user=Profile.objects.filter(user_id=self.request.user.id)
#             # convert this cart {'4':6,'6':2} to {"4":6,"6":2}
#             # single quotation need to be converted to double quote
#             carty=str(self.cart)
#             # get the cart of the current user
#             carty=carty.replace("\'","\"")
#             # save the carty to the profile
#             current_user.update(old_cart=str(carty))
#     def add(self,product,quantity):
#         product_id=str(product)
#         product_qty=str(quantity)
#         if product_id in self.cart:
#             # checking if already in cart
#             pass
#         else:
#             # self.cart[product_id]={'price':str(product.price)}
#                  # here product_id is the key of the cart whose value is a dictionary
#             self.cart[product_id]=int(product_qty)

#         self.session.modified=True
#         # dealing with the loggedin user
#         # for persistence of cart in logged out
#         if self.request.user.is_authenticated:
#             # lets gets the current user profile
#             current_user=Profile.objects.filter(user_id=self.request.user.id)
#             # convert this cart {'4':6,'6':2} to {"4":6,"6":2}
#             # single quotation need to be converted to double quote
#             carty=str(self.cart)
#             # get the cart of the current user
#             carty=carty.replace("\'","\"")
#             # save the carty to the profile
#             current_user.update(old_cart=str(carty))
#             # save to the old cart in profile model
#             # now this will be saved even if the session is logged out
#             # this data need to be pulled out from the model i.e. db during login
#     def __len__(self):
#         return len(self.cart)
#     def getproducts(self):
#         # get ids from cart
#         products_ids=self.cart.keys()
#         #use ids to lookup products in a database model
#         products=Product.objects.filter(id__in=products_ids)
#         return products
#     def getquants(self):
#         quantities=self.cart
#         return quantities
#     def update(self,product,quantity):
#         product_id=str(product)
#         product_qty=int(quantity)
#         #get out cart to update it
#         ourcart=self.cart
#        #update dictionary/cart
#         ourcart[product_id]=product_qty

#         self.session.modified=True
#         thing=self.cart
#         return thing
#     def totals(self):
#         product_ids=self.cart.keys()
#         # give the ids of all the product in carts
#         quantities=self.cart
#         # {"4":3,:"2":4} this format is obtained form self.cart where key is id and value is quantity of the item in cart
#         products=Product.objects.filter(id__in=product_ids)
#         total=0
#         for key,value in quantities.items():
#            key=int(key)
#            for product in products:
#                if product.id==key:
#                    total=total+(product.price*value)

#         return total

#     def delete(self,product):
#         product_id=str(product)
#         if product_id in self.cart:
#             del self.cart[product_id]
#         self.session.modified=True


from commerce.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key!  Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}


        # Make sure cart is available on all pages of site
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
                       
    # def add(self, product, quantity):
    # 	product_id = str(product.id)
    # 	product_qty = str(quantity)
    # 	# Logic
    # 	if product_id in self.cart:
    # 		pass
    # 	else:
    # 		#self.cart[product_id] = {'price': str(product.price)}
    # 		self.cart[product_id] = int(product_qty)

    # 	self.session.modified = True

    # 	# Deal with logged in user
    # 	if self.request.user.is_authenticated:
    # 		# Get the current user profile
    # 		current_user = Profile.objects.filter(user__id=self.request.user.id)
    # 		# Convert {'3':1, '2':4} to {"3":1, "2":4}
    # 		carty = str(self.cart)
    # 		carty = carty.replace("\'", "\"")
    # 		# Save carty to the Profile Model
    # 		current_user.update(old_cart=str(carty))
    
    


    # Add or update product in the cart
    # if product_id in self.cart:
    #     # Update the quantity if the product is already in the cart
    #     self.cart[product_id] += quantity
    # else:
    #     # Add new product to the cart with the specified quantity
    #     self.cart[product_id] = quantity

    # self.session.modified = True

    def add(self,product):
            product_id=str(product.id)
            # product_qty=str(quantity)
            if product_id in self.cart:
                # checking if already in cart
                pass
            else:
                # self.cart[product_id]={'price':str(product.price)}
                    # here product_id is the key of the cart whose value is a dictionary
                self.cart[product_id]=int(2)

            self.session.modified=True
            # dealing with the loggedin user
            # for persistence of cart in logged out
            if self.request.user.is_authenticated:
                # lets gets the current user profile
                current_user=Profile.objects.filter(user_id=self.request.user.id)
                # convert this cart {'4':6,'6':2} to {"4":6,"6":2}
                # single quotation need to be converted to double quote
                carty=str(self.cart)
                # get the cart of the current user
                carty=carty.replace("\'","\"")
                # save the carty to the profile
                current_user.update(old_cart=str(carty))
                # save to the old cart in profile model
                # now this will be saved even if the session is logged out
                # this data need to be pulled out from the model i.e. db during login

    def totals(self):
        # # Get product IDS
        # product_ids = self.cart.keys()
        # # lookup those keys in our products database model
        # products = Product.objects.filter(id__in=product_ids)
        # # Get quantities
        # quantities = self.cart
        # # Start counting at 0
        # total = 0
         # Get product IDS
        product_ids = [key for key in self.cart.keys() if key.isdigit()]  # Ensure only numeric keys
        # lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0
        
        for key, value in quantities.items():
            # Convert key string into into so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)



        return total



    def __len__(self):
        return len(self.cart)

    def getproducts(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)

        # Return those looked up products
        return products

    def getquants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        # Get cart
        ourcart = self.cart
        # Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True
    

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


        thing = self.cart
        return thing

    def delete(self, product):
        print("delete")
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}\
            if current_user:
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
        current_user.update(old_cart=str(carty))