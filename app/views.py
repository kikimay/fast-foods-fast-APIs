from app import app
from flask import Flask, request, session, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re


app = Flask(__name__)

app.secret_key = os.urandom(12)

@app.route("/")
def index():
    return jsonify(200,"WELCOME. You are here.")


#USER SECTION
users = [{
        "admin": True,
        "email": "maryn@gmail.com",
        "name": "kiki",
        "password": "pass",
        "user_id": 1,
        "username": "may"
        }]

class Users(object):
    @app.route("/api/v1/register", methods=["POST"])
    def register():#define a method that registers a user
        if not request.is_json:
            return jsonify(400,"request not json")
        else:
            data = request.get_json() 
            user_id =  len(users)+1
            name = data['name']
            email = data['email']
            username = data['username']
            password = data['password']
            password2 = data['password2']

        
        if not password == password2:#check if the two passwords match
            return jsonify(400,"passwords don't match")

        if name == "" or email == "" or username == "" or password == "" or password2 == "":
            return jsonify(400,"Please fill all the required fields")#check if name,email,username,password,password2 are empty
       
        if not re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email, re.IGNORECASE):
            return jsonify(400,"Email Provided is not in email format")#check email format
       
        
        if len(users) > 0:
            for user in users:
                e = user.get('email')#gets all the email adresses for all the existing users.
                
                
        else:
            user = {
                 "user_id":user_id,
                 "name":name,
                 "email":email,   
                 "username":username,
                 "password":password,
                 "admin":False
                 }

            users.append(user)#create the first user

            return make_response(jsonify({"status":"created", "user":user, "users":users }),201)
                
                
        if email == e:
            return jsonify(400,"user already exists")#check if email adress provided matches one that already exists
                    
                   
        else:
            user = {
                 "user_id":user_id,
                 "name":name,
                 "email":email,   
                 "username":username,
                 "password":password,
                 "admin":False
                 }

            users.append(user)#add user to the list of users if the email provided doesnt match one of the existing users

            return make_response(jsonify({"status":"created", "user":user, "users":users }),201)


      #code for user login
    @app.route("/api/v1/login")
    def home():
        if session.get('logged_in'):#checks if user is logged in and if admin is logged in
            return make_response(jsonify({"status":"user logged in", "id":session['user_id'], "login":True}, ),200)
        elif session.get('logged_in_admin'):
            return make_response(jsonify({"status":"admin logged in", "login":True}, ),200)
        else:
            return make_response(jsonify({"status":"login error", "login":False}),401)
     
    @app.route("/api/v1/login", methods=["POST"])
    def do_user_login():
        data = request.get_json()
        email = data['email']
        password = data['password']


        if email == "" or password == "":#check whether email and password are empty
            return jsonify(400,"Please fill all the required fields")
       
        if not re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email, re.IGNORECASE):
            return jsonify(400,"Email Provided is not in email format")#check email format
       
        

        for user in users:
            e = user.get('email')
            p = user.get('password')
            r = user.get('admin')
           #retrieve email,passwword and kind of user
            if password == p and email == e and r == False:
                session['user_id'] = user.get('user_id')
                session['logged_in'] = True #when r is false user is the one logged in
            elif password == p and email == e and r == True:
                session['user_id'] = user.get('user_id')
                session['logged_in_admin'] = True#when r is true admin is the one logged in
            else:
                session['logged_in'] = False
                session['logged_in_admin'] = False
            
        return Users.home()

    



    @app.route("/api/v1/logout")
    def logout():
        session['logged_in'] = False
        session['logged_in_admin'] = False
        return Users.home()#when session logged_in is false means user is logout



#FOOD SECTION
foods = []

class Foods(object):
    @app.route("/api/v1/add_food", methods=["POST"])
    def add_food():#define a method that adds new food item
        if not session.get('logged_in_admin'):#check if admin is logged in
            return jsonify(400,"Admin User must be logged in")

        
        if not request.is_json:
            return jsonify(400,"request not json")
        else:
            data = request.get_json() 
            food_id =  len(foods)+1
            name = data['name']
            price = data['price']
            image = data['image']
            createdby = session['user_id']#get data from ui in json

        
        

        if len(foods) > 0:
            for food in foods:
                n = food.get('name')
                p = food.get('price')#for every food item in the list of foods get its price an name
                
                
        else:#if the list of foods is empty add the new food item
            food = {
                 "food_id":food_id,
                 "name":name,
                 "price":price,   
                 "image":image,
                 "createdby":createdby
                 }

            foods.append(food)

            return make_response(jsonify({"status":"created", "food":food, "foods":foods }),201)
                
                
        if name == n and price == p:#check if the food item already exists
            return jsonify(400,"food item already exists")
        elif not price.isdigit():
            return jsonify(400,"Price is not valid")
                     
        else:#if food item does not exist add it to the list
            food = {
                 "food_id":food_id,
                 "name":name,
                 "price":price,   
                 "image":image,
                 "createdby":createdby
                 }

            foods.append(food)

            return make_response(jsonify({"status":"created", "food":food, "foods":foods }),201)



    @app.route("/api/v1/foods", methods=["GET"])
    def foodsall():#a function that returns all foods
        return make_response(jsonify({"status":"ok", "foods":foods}),200)



    @app.route('/api/v1/foods/<int:food_id>', methods=['GET'])
    def specificfood(food_id):#a function that gets a specific food item by id
        food = [food for food in foods if food.get('food_id')==food_id]
        
        
        if len(food) == 0:#check whether food list is empty
            return (422,"Food you are looking for does not exist")
        

        else:
            return make_response(jsonify({"status":"ok", "food":food}),200)



    @app.route('/api/v1/foods/<int:food_id>', methods=['DELETE'])
    def deletefood(food_id):# a function to delete food item
        if not session.get('logged_in_admin'):
            return jsonify(400,"Admin User must be logged in")#admin must be logged inorder to delete
        
        if request.method == 'DELETE':#check method
           
            if len(foods) != 0:#check the list to make sure its not empty
                for food in foods:
                    f = food.get('food_id')#get food ids for food items
                    if f == food_id:#compare the ids
                        foods.remove(food)#delete the food item
                        return make_response(jsonify({"status":"ok", "foods":foods}),200)


            else:
                return make_response(jsonify({'error': 'the food does not exist'}), 404)

        else:
            return Foods.specificfood(food_id)
            
           

    @app.route('/api/v1/foods/<int:food_id>', methods=['PUT'])
    def updatefoods(food_id):
        if not session.get('logged_in_admin'):
            return jsonify(400,"Admin User must be logged in")
        
        if request.method == 'PUT':
            data = request.get_json()
            if len(foods) != 0:
                for food in foods:
                    f = food.get('food_id')
                    if f == food_id:
                        if not data['price'].isdigit():#check whether price isa digit
                            return jsonify(400,"Price is not valid")
                    
                        if not data['price'] == "" and data['image'] == "":#check if data null
                            food['price'] = data['price']
                            return make_response(jsonify({"status":"ok", "food":food}),200)
                        elif not data['image'] == "" and data['price'] == "":
                            food['image'] = data['image']
                            return make_response(jsonify({"status":"ok", "food":food}),200)
                        elif not data['price'] == "" and not data['image'] == "":
                            food['price'] = data['price']
                            food['image'] = data['image']
                            return make_response(jsonify({"status":"ok", "food":food}),200)
                        else:
                            return make_response(jsonify({"status":"No updates done", "food":food}),200)
                    
                    else:
                        return make_response(jsonify({'error': 'the food does not exist'}), 404)

                            
            else:
                return make_response(jsonify({'error': 'the food does not exist'}), 404)

        else:
            return Foods.specificfood(food_id)
            

#ORDERS SECTION
orders = []
order_items = []

class Orders(object):
    @app.route("/api/v1/place_order", methods=["POST", "GET"])
    def place_order():
        if not session.get('logged_in'):#user must be logged in so he can place an order

            return jsonify(400,"User must be logged in")



        if not request.is_json:
            return jsonify(400,"request not json")#data must be json 
        else:
            data = request.get_json() 
            order_id =  len(orders)+1
            
            ordered_by = session['user_id']
            destination = data['destination']
            payment_mode = data['payment_mode']
            ordered_items = data['order_items']
            

            
           
        if destination == "" or payment_mode == "":#user must fill both destination and payment mode else order cant be placed
            return jsonify(400,"You must fill all fields")
        
        else:
            
            for ordered_item in ordered_items:
                food_name = ordered_item.get('food_name')
                quantity = ordered_item.get('quantity')
                
                order_item_id =  len(order_items)+1
                
                if quantity == "":#user must specify quantity else order cant be placed
                    return jsonify(400,"You must fill all fields")
                if not quantity.isdigit():
                    return jsonify(400,"quantity is not valid")
                    

                for food in foods:#loop through foods list and get the name and price for each food item in foods list.
                    name = food.get('name')
                    price = food.get('price')

                    if food_name == name:
                        total = int(quantity) * int(price)#calculates the total amount to be paid when quantity for a food is greater than one.
   
                        order_item = {
                            "order_item_id":order_item_id,
                            "order_id":order_id,
                            "food_name":food_name,
                            "Quantity":quantity,
                            "price":price,
                            "total":total
                            }
                        

                        order_items.append(order_item)

                grand = 0
                items = 0
                for order_item in order_items:
                    o = order_item.get('order_id')
                    
                    if o == order_id:
                        num = order_item.get('Quantity')
                        total = order_item.get('total')
                        grand = grand + int(total)#calculate total amount to be paid eventually.
                        items = items + int(num)#calculate the total number of items ordered.

            order = {
                "order_id":order_id,
                "ordered_by":ordered_by,
                "destination":destination,   
                "payment_mode":payment_mode,
                "completed_status":False,
                "accepted_status":None,
                "grand_total":grand,
                "number_of_items":items
                }

            orders.append(order) #add order to the list of orders.          

            return make_response(jsonify({"status":"created", "orders":orders, "order_items":order_items, "order":order, "order_item":order_item,}),201)

    
    @app.route("/api/v1/orders", methods=["GET"])
    def ordersall():
        if not session.get('logged_in_admin'):
            return jsonify(400,"Admin User must be logged in")#to get a list of all orders admin users must be logged in
        else:
            return make_response(jsonify({"status":"ok", "orders":orders}),200)
        



    @app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
    def specificorder(order_id):
        if not session.get('logged_in_admin'):
            return jsonify(400,"Admin User must be logged in")#to get a specific order a user must be logged in
        
        order = [order for order in orders if order.get('order_id')==order_id]#get a specific order by order id
        
        
        
        if len(order) == 0:
            return (422,"Order you are looking for does not exist")
        

        else:
            return make_response(jsonify({"status":"ok", "order":order}),200)



    @app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
    def updateorders(order_id):
        if not session.get('logged_in_admin'):
            return jsonify(400,"Admin User must be logged in")#to update an order admin user must be logged in
        
        
        if request.method == 'PUT':#method for update is PUT
            data = request.get_json()
            if len(orders) != 0:
                for order in orders:
                    o = order.get('order_id')#fetch order id of each order in orders and compare it with one that the admin inputs.
            
                    if o == order_id:
                        if not data['completed_status'] == "" and data['accepted_status'] == "":
                            if not order.get('accepted_status') == True:
                                return make_response(jsonify({'error': 'Order must be accepted before it can be marked as complete.'}), 400)

                            else:
                                order['completed_status'] = data['completed_status']
                            
                                return make_response(jsonify({"status":"ok", "order":order}),200)

                        elif not data['accepted_status'] == "" and data['completed_status'] == "":
                            order['accepted_status'] = data['accepted_status']
                    
                            return make_response(jsonify({"status":"ok", "order":order}),200)


                        elif  data['accepted_status'] == "" and data['completed_status'] == "":
                            
                            return make_response(jsonify({'error': 'Please provide the status to be updated'}), 400)

                        else:
                            return make_response(jsonify({'error': 'Only one status can be updated at a time.'}), 400)
                    else:
                        return jsonify(404,"Order does not exist")#order has to exist for updating

            else:
                return make_response(jsonify({'error': 'the order does not exist'}), 404)

        else:
            return Orders.specificorder(order_id)#returns specific order





















































