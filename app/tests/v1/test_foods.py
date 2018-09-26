import pytest
from flask import json
from app.api.v1.views import app
from app.api.v1.views import Foods
from app.api.v1.views import Users
from app.tests.v1 import sign_in_admin_helper, sign_up_sign_in_helper, sign_in_helper

 

testusers = Users()
testfoods = Foods()



sample_food=[
    {"name":"Hamburger", "price":"abc",	"image":"image"},
    {"name":"Hamburger", "price":"-200",	"image":"image"},
    {"name":"123", "price":"200",	"image":"image"},
    {"name":"", "price":"200",	"image":"image"},
    {"name":"Hamburger", "price":"",	"image":"image"},
    {"name":"Hamburger", "price":"200",	"image":""},
    {"name":"Hamburger", "price":"200",	"image":"image"}
]



sample_food_updates=[
    {"price":"300",	"image":"image1"},
    {"price":"-300",	"image":"image1"},
    {"price":"abc",	"image":"image1"},
    {"price":"300",	"image":""},
    {"price":"",	"image":"image1"},
    {"price":"300",	"image":"image1"},
    {"price":"",	"image":""}
]




'''-------------------------------------------------------------------------------------------------------------------------------'''

#GET ALL FOODS TESTS


def test_foods_retrive_all():
    result=app.test_client()
    response= result.get('/api/v1/foods',content_type='application/json')
    assert(response.status_code==404)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#ADD FOOD TESTS


def test_foods_price_not_digit():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.post('/api/v1/add_food', data=sample_food[0] ,content_type='application/json')
    assert(response.status_code==400)

def test_foods_price_not_digit1():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.post('/api/v1/add_food', data=sample_food[1] ,content_type='application/json')
    assert(response.status_code==400)

def test_foods_food_name_not_str():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.post('/api/v1/add_food', data=sample_food[2] ,content_type='application/json')
    assert(response.status_code==400)

def test_foods_food_name_empty():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.post('/api/v1/add_food', data=sample_food[3] ,content_type='application/json')
    assert(response.status_code==400)

def test_foods_price_empty():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.post('/api/v1/add_food', data=sample_food[4] ,content_type='application/json')
    assert(response.status_code==400)

def test_foods_image_empty():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.post('/api/v1/add_food', data=sample_food[5] ,content_type='application/json')
    assert(response.status_code==400)

def test_foods_successfully():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.post('/api/v1/add_food', data=json.dumps(sample_food[6]) ,content_type='application/json')
    json.loads(response.data)
    assert(response.status_code==201)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#GET SPECIFIC FOOD TESTS


def test_get_food_negative_identifier():
    result=app.test_client()
    response= result.get('/api/v1/foods/-1' ,content_type='application/json')
    assert(response.status_code == 404)

def test_get_food_not_created():
    result=app.test_client()
    response= result.get('/api/v1/foods/100' ,content_type='application/json')
    assert(response.status_code == 404)

def test_get_food_successfully():
    result=app.test_client()
    response= result.get('/api/v1/foods/1' ,content_type='application/json')
    assert(response.status_code == 200)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#UPDATE FOOD TESTS

#FIND FOOD TESTS

def test_update_food_nonexistent():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.put('/api/v1/foods/100', data=sample_food_updates[0] ,content_type='application/json')
    assert(response.status_code==400)

def test_foods_update_price_not_digit():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.put('/api/v1/add_food', data=sample_food_updates[1] ,content_type='application/json')
    assert(response.status_code==405)

def test_foods_update_price_not_digit1():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.put('/api/v1/foods/1', data=sample_food_updates[2] ,content_type='application/json')
    assert(response.status_code==400)

def test_update_food_none():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.put('/api/v1/foods/1', data=json.dumps(sample_food_updates[6]) ,content_type='application/json')
    assert(response.status_code==406)

def test_update_food_price_only_successfully():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.put('/api/v1/foods/1', data=json.dumps(sample_food_updates[3]) ,content_type='application/json')
    assert(response.status_code==200)

'''def test_update_food_image_only_successfully():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.put('/api/v1/foods/1', data=json.dumps(sample_food_updates[4]) ,content_type='application/json')
    assert(response.status_code==200)'''

def test_update_food_both_successfully():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.put('/api/v1/foods/1', data=json.dumps(sample_food_updates[5]) ,content_type='application/json')
    assert(response.status_code==200)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#DELETE SPECIFIC FOOD TESTS


def test_delete_food_negative_identifier():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.delete('/api/v1/foods/-1' ,content_type='application/json')
    assert(response.status_code == 404)

def test_delete_food_not_created():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.delete('/api/v1/foods/100' ,content_type='application/json')
    assert(response.status_code == 404)

def test_delete_food_successfully():
    result=app.test_client()
    sign_in_admin_helper(result)
    response= result.delete('/api/v1/foods/1' ,content_type='application/json')
    assert(response.status_code == 200)