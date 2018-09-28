from app.api.v2 import app
from app.api.v2 import models, database
from app.api.v2.models import UserModels, FoodModels, OrderModels
from flask import Flask, request, session, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re




#ORDERS SECTION
orders = []
order_items = []

class Orders(object):
    @app.route("/api/v2/place_order", methods=["POST", "GET"])
    def place_order(self):
        if not session.get('logged_in'):
            return jsonify(400,"User must be logged in")


        if not request.is_json:
            return jsonify(400,"request not json")
        else:
            data = request.get_json() 
            ordered_by = session['user_id']
            destination = data['destination']
            payment_mode = data['payment_mode']
            ordered_items = data['order_items']
            status = "new"

            
           
        if destination == "" or payment_mode == "":
            return jsonify(400,"You must fill all fields")
        
        else:
            
            for ordered_item in ordered_items:
                food_id = ordered_item.get('food_id')
                quantity = ordered_item.get('quantity')
                
                
                if quantity == "":
                    return jsonify(400,"You must fill all fields")

                food = FoodModels.get_by_id(self, food_id)
                price = food.get('price')

                if food > 0:
                    total = int(quantity) * int(price)
                    order_item = {
                        "food_id":food_id,
                        "Quantity":quantity,
                        "price":price,
                        "total":total
                        }
                    

                    order_items.append(order_item)

                grand = 0
                items = 0
                for order_item in order_items:
                    num = order_item.get('Quantity')
                    total = order_item.get('total')
                    grand = grand + int(total)
                    items = items + int(num)

            order = {
                "ordered_by":ordered_by,
                "destination":destination,   
                "payment_mode":payment_mode,
                "status":status,
                "grand_total":grand,
                "number_of_items":items
                }

            OrderModels.add_order(order)
            orders =  OrderModels.get_all(self)

            order_id = OrderModels.last_order_id(self)

            for order_item in order_items:
                order_item = {
                        "food_id":food_id,
                        "order_id":order_id,
                        "Quantity":quantity,
                        "price":price,
                        "total":total
                        }

                OrderModels.add_order_items(order_item)
                              

            return make_response(jsonify({"status":"created", "orders":orders, "order_items":order_items, "order":order}),201)

    
    @app.route("/api/v2/orders", methods=["GET"])
    def ordersall(self):
        if not session.get('logged_in_admin'):
            return jsonify(400,"Admin User must be logged in")
        else:
            orders = OrderModels.get_all(self)
            return make_response(jsonify({"status":"ok", "orders":orders}),200)
        



    @app.route('/api/v2/orders/<int:order_id>', methods=['PUT', 'GET'])
    def specificorder(self, order_id):
        if not session.get('logged_in_admin'):
            return jsonify(400,"Admin User must be logged in")

        order = OrderModels.get_by_id(self, order_id)
        
        if request.method == 'PUT':
            data = request.get_json()
            status = data['status']
            
            
            
            if order > 0:
                '''
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
            '''
            else:
                return make_response(jsonify({'error': 'the order does not exist'}), 404)

        else:
            
            
            if len(order) == 0:
                return make_response(jsonify({"status":"not found","message":"order you are looking for does not exist"}),404)
                    
            else:
                return make_response(jsonify({"status":"ok", "order":order}),200)

