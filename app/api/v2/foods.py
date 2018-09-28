from app.api.v2 import app
from app.api.v2 import models, database, users
from app.api.v2.models import UserModels, FoodModels, OrderModels
from flask import Flask, request, session, jsonify, make_response
import os
import re



app = Flask(__name__)


app.secret_key = os.urandom(12)

#FOOD SECTION
class Foods(object):
    @app.route("/api/v2/add_food", methods=["POST"])
    def add_food(self): #define a method that adds new food item
        if not session.get('logged_in_admin'):
            return make_response(jsonify({"status":"unauthorised", "message":"Admin User must be logged in"}),401)
        
        
        if not request.is_json:
            return make_response(jsonify({"status":"wrong format","message":"request not json"}),400)
        else:
            data = request.get_json() 
            name = data['name']
            price = data['price']
            image = data['image']
            createdby = session['user_id']#get data in json

        if name == "" or price == "" or image == "":
            return make_response(jsonify({"status":"not acceptable","message":"all fields must be filled"}),406)

        if not price.isdigit():
            return make_response(jsonify({"status":"not acceptable","message":"price not valid"}),405)

        if not name.isalpha():
            return make_response(jsonify({"status":"not acceptable","message":"food name not valid"}),405)

        
        foods = FoodModels.get_all(self)

        if len(foods) > 0:
            for food in foods:
                name1 = food.get('name')
                price2 = food.get('price')#for every food item in the list of foods get its price an name
                
            if name == name1 and price == price2:
                return make_response(jsonify({"status":"forbidden","message":"food already exists"}),403)
           
            else:#if the food does not exist add the new food item
                food = {
                    "name":name,
                    "price":price,   
                    "image":image,
                    "createdby":createdby
                    }

                
                
        else:#if the list of foods is empty add the new food item
            food = {
                 "name":name,
                 "price":price,   
                 "image":image,
                 "createdby":createdby
                 }

        FoodModels.add_foods(food)

        return make_response(jsonify({"status":"created", "food":food, "foods":foods }),201)
            
                
        

    @app.route("/api/v2/foods", methods=["GET"])
    def foodsall(self): #a function that returns all foods
        foods = FoodModels.get_all(self)
        return foods


    @app.route('/api/v2/foods/<int:food_id>', methods=['GET','DELETE','PUT'])
    def specificfood(self, food_id):#a function that gets a specific food item by id
        foods = FoodModels.get_all(self)
        
        if request.method == 'DELETE':
            if not session.get('logged_in_admin'):
                return jsonify(400,"Admin User must be logged in")
            

            if len(foods) != 0:#check the list to make sure its not empty
                for food in foods:
                    food2 = food.get('food_id')#get food ids for food items
                    if food2 == food_id:#compare the ids
                        FoodModels.delete_food(self, food_id) #delete the food item
                        return make_response(jsonify({"status":"ok", "foods":foods}),200)
                    else:
                        return make_response(jsonify({'error': 'the food does not exist'}), 404)
            else:
                return make_response(jsonify({'error':'the food does not exist'}),404)

        

        elif request.method == 'PUT':
            if not session.get('logged_in_admin'):
                return jsonify(400,"Admin User must be logged in")

                 
            data = request.get_json()
            price = data['price']
            image = data['image']
            edited_by = session['user_id']
            
            if not data['price'].isdigit():#check whether price isa digit
                return make_response(jsonify({"status":"not acceptable","message":"Price is not valid"}),406)
                    
            if len(foods) != 0:
                for food in foods:
                    food2 = food.get('food_id')
                    if food2 == food_id:
                        FoodModels.update_food(self, food_id)
                        food = FoodModels.get_by_id(self, food_id)
                        return make_response(jsonify({"status":"ok", "food":food}),200)
                    else:
                        return make_response(jsonify({'error': 'the food does not exist'}), 404)

                            
            else:
                return make_response(jsonify({'error': 'the food does not exist'}), 404)

        else:
            if len(foods) != 0:#check whether list foods is empty
                food = FoodModels.get_by_id(self, food_id)
                return make_response(jsonify({"status":"ok", "food":food}),200)

            else:
                return make_response(jsonify({'error':'the food does not exist'}),404)

            
