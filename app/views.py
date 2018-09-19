from app import app
from flask import Flask, request, session, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import os



app = Flask(__name__)

@app.route("/")
def index():
    return jsonify(200,"WELCOME. You are here.")
    #USER SECTION
users = []#an empty list which is to contain dictionaries.

class Users(object):
    @app.route("/api/v1/register", methods=["POST"])
    def register():
        if not request.is_json:
            return jsonify(400,"request not json")#check whether data is in json form.
        else:
            data = request.get_json() 
            user_id =  len(users)+1
            name = data['name']
            email = data['email']
            username = data['username']
            password = data['password']
            password2 = data['password2']

        
        if not password == password2:#check whether passwords match
            return jsonify(403,"passwords don't match")

        
        if len(users) > 0:
            for user in users:
                e = user.get('email')
                u = user.get('username')
                p = user.get('password')#loops the user list of dictionaries 
                
        else:
            user = {
                 "user_id":user_id,
                 "name":name,
                 "email":email,   
                 "username":username,
                 "password":password,
                 "admin":False
                 }#create a dictionary with user details

            users.append(user)#create the first user.

            return make_response(jsonify({"status":"created", "user":user, "users":users }),201)
                
                
        if email == e:
            return jsonify(403,"user already exists")#check whether a user already exists via email.
                    
       
        else:
            user = {
                 "user_id":user_id,
                 "name":name,
                 "email":email,   
                 "username":username,
                 "password":password,
                 "admin":False
                 }

            users.append(user)#create a new user and add them to the already existing list of users.

            return make_response(jsonify({"status":"created", "user":user, "users":users }),201)






    @app.route("/api/v1/login")
    def home():
        if session.get('logged_in'):#check whether user is logged in
            return make_response(jsonify({"status":"user logged in", "id":session['user_id'], "login":True}, ),200)
        elif session.get('logged_in_admin'):#check whether admin user is logged in
            return make_response(jsonify({"status":"admin logged in", "login":True}, ),200)
        else:
            return make_response(jsonify({"status":"login error", "login":False}),401)
     
    @app.route("/api/v1/login", methods=["POST"])
    def do_user_login():#define a method that does user login
        data = request.get_json()
        username = data['username']
        password = data['password']

        for user in users:
            u = user.get('username')
            p = user.get('password')
            r = user.get('admin')

            if password == p and username == u and r == False:#this if statament checks if username and password entered match one of the users in memory and also whether the user is an admin user or a user_user and returns the user id.
                session['user_id'] = user['user_id']
                session['user_id'] = user['user_id']
                session['logged_in'] = True
            elif password == p and username == u and r == True:
                session['logged_in_admin'] = True#admin loggedin.
            else:
                session['logged_in'] = False
                session['logged_in_admin'] = False
            
        return Users.home()#return to home page index.html


    


    #code for app logout.  
    @app.route("/api/v1/logout")
    def logout():
        session['logged_in'] = False
        return Users.home()



#FOOD SECTION
foods = []

class Foods(object):
    @app.route("/api/v1/add_food", methods=["POST"])
    def add_food():#define a method that adds food item.
        if not session.get('logged_in'):
            return jsonify(400,"User must be logged in")#check if user is logged return error messege if not

        
        if not request.is_json:
            return jsonify(400,"request not json")
        else:
            data = request.get_json() 
            food_id =  len(foods)+1
            name = data['name']
            price = data['price']
            image = data['image']
            createdby = session['user_id']

        
        

        if len(foods) > 0:
            for food in foods:
                n = food.get('name')
                p = food.get('price')
                
                
        else:
            food = {
                 "food_id":food_id,
                 "name":name,
                 "price":price,   
                 "image":image,
                 "createdby":createdby
                 }#a new food item to be added  to an empty list of foods

            foods.append(food)

            return make_response(jsonify({"status":"created", "food":food, "foods":foods }),201)
                
                
        if name == n and price == p:#check whether food name and price already exist.
            return jsonify(403,"food item already exists")
                    
        else:
            food = {
                 "food_id":food_id,
                 "name":name,
                 "price":price,   
                 "image":image,
                 "createdby":createdby
                 }#add a new food item that doesnt exist

            foods.append(food)

            return make_response(jsonify({"status":"created", "food":food, "foods":foods }),201)
            
    @app.route("/api/v1/get_allfoods",methods=["GET"])
    def get_allfoods():
        if foods != []:
            return make_response(jsonify({"foods":foods}),200)
        else:
            return make_response(jsonify("no foods available"), 404)




#ORDERS SECTION
orders = []
order_items = []

class Orders(object):
    @app.route("/api/v1/place_orders", methods=["POST", "GET"])
    def place_order():
        if not session.get('logged_in'):
            return jsonify(400,"User must be logged in")#user must be logged in so he can place an order


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
            
            for ordered_item in ordered_items:#loop through orders list
                food_name = ordered_item.get('food_name')
                quantity = ordered_item.get('quantity')
                
                order_item_id =  len(order_items)+1
                
                if quantity == "":#user must specify quantity else order cant be placed
                    return jsonify(400,"You must fill all fields")

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
                        

                        order_items.append(order_item)#add order to the order items by other users

                        grand = 0
                        granditems = 0
                        for order_item in order_items:
                            total = order_item.get('total')
                            grand = grand + int(total)
                            grand = grand + int(total)#calculate total amount to be paid eventually.
                            quantity = order_item.get('quantity')
                            granditems = granditems + int(quantity)
                            granditems = granditems + int(quantity)#calculate the total number of items ordered.
                        
            order = {
                "order_id":order_id,
                "ordered_by":ordered_by,
                "destination":destination,   
                "payment_mode":payment_mode,
                "completed_status":False,
                "accepted_status":False,
                "grand":grand
                }

            orders.append(order)#add order to the list of orders.                 

            return make_response(jsonify({"status":"created", "orders":orders, "order_items":order_items, "order":order, "order_item":order_item,}),201)

    
    @app.route("/api/v1/orders", methods=["GET"])
    def ordersall():
        if not session.get('logged_in'):
            return jsonify(400,"User must be logged in")#to get a list of all orders admin users must be logged in
        else:
            return make_response(jsonify({"status":"ok", "orders":orders}),200)
        



    @app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
    def specificorder(order_id):
        if not session.get('logged_in'):
            return jsonify(400,"User must be logged in")#to get a specific order a user must be logged in
        
        order = [order for order in orders if order.get('order_id')==order_id]#get a specific order by order id
        
        
        if len(order) == 0:
            return (422,"Order you are looking for does not exist")
        

        else:
            return make_response(jsonify({"status":"ok", "order":order}),200)



    @app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
    def updateorders(order_id):
        if not session.get('logged_in'):
            return jsonify(400,"User must be logged in")#to update an order admin user must be logged in
        
        if request.method == 'PUT':#method for update is PUT
            data = request.get_json()
            if len(orders) != 0:
                for order in orders:
                    o = order.get('order_id')#fetch order id of each order in orders and compare it with one that the admin inputs.
                    if o == order_id:
                        if not data['completed_status'] == "" and data['accepted_status'] == "":
                            if order.get('accepted_status') == False:#boleen order status not accepted
                                return make_response(jsonify({'error': 'Order must be accepted before it can be marked as complete.'}), 400)

                            else:
                                order['completed_status'] = data['completed_status']
                            
                                return make_response(jsonify({"status":"ok", "order":order}),200)

                        elif not data['accepted_status'] == "" and data['completed_status'] == "":#when order status has been accepted then mark status as complete
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
            
