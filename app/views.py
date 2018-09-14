#USER SECTION
users = []

class Users(object):
    @app.route("/register", methods=["POST"])
    def register():
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

        
        if  password != password2:
            return jsonify(403,"passwords don't match")

        
        if  len(users) != 0:
            for user in users:
                email2 = user.get('email')
            if email == email2:
                return jsonify(403,"user already exists")
        
                
        else:
            user = {
                "user_id":user_id,
                "name":name,
                "email":email,   
                "username":username,
                "password":password
                }

            users.append(user)

            return make_response(jsonify({"status":"created", "user":user}),201)

    app.route("/login")
    def home():
        if session.get('logged_in'):
            return make_response(jsonify({"status":"user logged in", "login":True}, ),200)
        else:
            return make_response(jsonify({"status":"login error", "login":False}),401)
     
    @app.route("/login", methods=["POST"])
    def do_login():
        data = request.get_json()
        username = data['username']
        password = data['password']

        for user in users:
            u = user.get('username')
            p = user.get('password')


            if password == p and username == u:
                session['logged_in'] = True
            else:
                session['logged_in'] = False
            
        return Users.home()

    @app.route("/logout")
    def logout():
        session['logged_in'] = False
        return Users.home()

                
        

#FOOD SECTION
food_items = []
class food(object):
    @app.route("/add_food_item", methods=["POST"])
    def add_food_item():
        if not request.is_json:
           return jsonify(400,"request not json")
        else:
            data = request.get_json()
            food_id = len(food_items)+1
            food_name= data['food_name']
            image = data['image']
            price = data['price']
            
        if len(food_items) != 0:
            for food_item in food_items:
                food_name2 = food_item.get('food_name')
            if food_name==food_name2:
                return jsonify(403,"food_item already exists")
        
        else:
            food_item = {
            "food_id":food_id,
            "food_name":food_name,
            "image":image,   
            "price":price,
            
            }

            food_items.append(food_item)

            return make_response(jsonify({"status":"created", "food_item":food_item}),201)


#ORDERS SECTION
orders = []
order_items = []

class Orders(object):
    @app.route("/place_order", methods=["POST", "GET"])
    def place_order():
       

        if not request.is_json:
            return jsonify(400,"request not json")
        else:
            data = request.get_json()
            order_id = len(orders)+1
                
            ordered_by = session['user_id']
            location = data['location']
            payment_mode = data['payment_mode']
            ordered_items = data['order_items']
                

                
            
            if location == "" or payment_mode == "":
                return jsonify(400,"You must fill all fields 1")
            
            else:
                order = {
                "order_id":order_id,
                "ordered_by":ordered_by,
                "location":location,
                "payment_mode":payment_mode,
                "completed_status":False,
                "accepted_status":False
                }

                orders.append(order)
                            
                for ordered_item in ordered_items:
                    food_name = ordered_item.get('food_name')
                    quantity = ordered_item.get('quantity')
                                
                order_item_id = len(order_items)+1
                
                if quantity == "":
                    return jsonify(400,"You must fill all fields 2")

                for food in foods:
                    name = food.get('name')
                    price = food.get('price')

                    if food_name == name:
                        total = True
                        order_item = {
                        "order_item_id":order_item_id,
                        "order_id":order_id,
                        "food_name":food_name,
                        "Quantity":quantity,
                        "price":price,
                        "total":total
                        }
                                                

                        order_items.append(order_item)

                        

            return make_response(jsonify({"status":"created", "orders":orders, "order_items":order_items, "order":order, "order_item":order_item,}),201)



@app.route("/orders", methods=["GET"])
    def ordersall():
        if not session.get('logged_in'):
            return jsonify(400,"User must be logged in")
        else:
            return make_response(jsonify({"status":"ok", "orders":orders}),200)
        