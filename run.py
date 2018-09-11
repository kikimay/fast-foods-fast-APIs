from app import app
from flask import Flask, flash, redirect, render_template, request, session, jsonify, make_response
import os



app = Flask(__name__)

@app.route('/')
def index():
    return ("WELCOME. You are here.")


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
   

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)




    
