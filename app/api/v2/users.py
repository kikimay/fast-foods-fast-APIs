from app.api.v2 import app
from app.api.v2 import models, database
from app.api.v2.models import UserModels, FoodModels, OrderModels
from flask import Flask, request, session, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re



app = Flask(__name__)


app.secret_key = os.urandom(12)
@app.route("/")
def index():
    return jsonify(200,"WELCOME. You are here Version 2.")



#USER SECTION
class Users(object):
    @app.route("/api/v2/user", methods=["POST"])
    def user(self):#define a method that registers a user
        if not request.is_json:
            return make_response(jsonify({"status":"wrong format","message":"request not json"}),400)
        else:
            data = request.get_json() 
            name = data['name']
            email = data['email']
            username = data['username']
            password = data['password']
            password2 = data['password2']

        
        if password != password2:#check if the two passwords match
            return make_response(jsonify({"status":"not acceptable","message":"passwords don't match"}),406)

        if name == "" or email == "" or username == "" or password == "" or password2 == "":
            return make_response(jsonify({"status":"not acceptable","message":"Please fill all the required fields"}),406)#check if name,email,username,password,password2 are empty
       
        if not re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email, re.IGNORECASE):
            return make_response(jsonify({"status":"not acceptable","message":"Email Provided is not in email format"}),406)#check email format
       
        users = UserModels.count_users(self)
        if users > 0:
            email2 = UserModels.fetch_by_email(self, email)
            if len(email2) > 0:
                return make_response(jsonify({"status":"not acceptable","message":"user already exists"}),406)#check if email adress provided matches one that already exists
            
            else:
                user = {
                    "name":name,
                    "email":email,   
                    "username":username,
                    "password":password,
                    "admin":False
                    }

                     
                    
                   
        else:
            user = {
                 "name":name,
                 "email":email,   
                 "username":username,
                 "password":password,
                 "admin":False
                 }

        UserModels.add_users(user)#add user to the table of users in the database

        user = UserModels.fetch_by_email(self, email)
        users = UserModels.all_users(self)

        return make_response(jsonify({"status":"created", "user":UserModels.serialize(user), "users":users }),201)


      #code for user login
    @app.route("/api/v2/login")
    def home(self):
        if session.get('logged_in'):#checks if user is logged in and if admin is logged in
            return make_response(jsonify({"status":"user logged in", "id":session['user_id'], "login":True}, ),200)
        elif session.get('logged_in_admin'):
            return make_response(jsonify({"status":"admin logged in", "login":True}, ),200)
        else:
            return make_response(jsonify({"status":"login error", "login":False}),401)
     
    @app.route("/api/v2/login", methods=["POST"])
    def do_user_login(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        password = generate_password_hash(password)


        if email == "" or password == "":#check whether email and password are empty
            return make_response(jsonify({"status":"not acceptable","message":"Please fill all the required fields"}),406)
       
        if not re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email, re.IGNORECASE):
            return make_response(jsonify({"status":"not acceptable","message":"Email Provided is not in email format"}),406)#check email format
       
        users = UserModels.all_users(self)

        for user in users:
            email2 = user.get('email')
            password2 = user.get('password')
            admin = user.get('admin')
           #retrieve email,passwword and kind of user
            if password == password2 and email == email2 and admin == False:
                session['user_id'] = user.get('user_id')
                session['logged_in'] = True #when r is false user is the one logged in
                
            elif password == password2 and email == email2 and admin == True:
                session['user_id'] = user.get('user_id')
                session['logged_in_admin'] = True#when r is true admin is the one logged in
                
                return Users.home(self)
            else:
                session['logged_in'] = False
                session['logged_in_admin'] = False
            
        return Users.home(self)

    



    @app.route("/api/v2/logout")
    def logout(self):
        if session.get('logged_in') or session.get('logged_in_admin'):
            session['logged_in'] = False
            session['logged_in_admin'] = False
            return Users.home(self)#when session logged_in is false means user is logout
        else:
            return make_response(jsonify({"status":"okay","message":"logged out already"}),200)






           
        
        
        
