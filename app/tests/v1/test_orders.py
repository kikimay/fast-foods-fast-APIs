import pytest
from flask import json
from app.api.v1.views import app
from app.api.v1.views import  Orders
from app.api.v1.views import  Users

testusers = Users()
testorders = Orders()



#ORDER INPUT FOR TESTS

sample_order=[{
            "destination":"Kenyatta",
            "payment_mode":"Cash",
            "order_items": [
                            {
                            "food_name":"Hamburger",
                            "quantity":"abc"
                            },
                            {
                            "food_name":"pizza",
                            "quantity":"def"
                            }
                           ]
            },
            {
            "destination":"Kenyatta",
            "payment_mode":"Cash",
            "order_items": [
                            {
                            "food_name":"123",
                            "quantity":"4"
                            },
                            {
                            "food_name":"456",
                            "quantity":"9"
                            }
                           ]
            },
            {
            "destination":"Kenyatta",
            "payment_mode":"Cash",
            "order_items": [
                            {
                            "food_name":"",
                            "quantity":"4"
                            },
                            {
                            "food_name":"",
                            "quantity":"9"
                            }
                           ]
            },
            {
            "destination":"Kenyatta",
            "payment_mode":"Cash",
            "order_items": [
                            {
                            "food_name":"Hamburger",
                            "quantity":""
                            },
                            {
                            "food_name":"pizza",
                            "quantity":""
                            }
                           ]
            },
            {
            "destination":"",
            "payment_mode":"Cash",
            "order_items": [
                            {
                            "food_name":"Hamburger",
                            "quantity":"4"
                            },
                            {
                            "food_name":"pizza",
                            "quantity":"9"
                            }
                           ]
            },
            {
            "destination":"Kenyatta",
            "payment_mode":"",
            "order_items": [
                            {
                            "food_name":"Hamburger",
                            "quantity":"4"
                            },
                            {
                            "food_name":"pizza",
                            "quantity":"9"
                            }
                           ]
            },
            {
            "destination":"Kenyatta",
            "payment_mode":"Cash",
            "order_items": []
            },
            {
            "destination":"Kenyatta",
            "payment_mode":"Cash",
            "order_items": [
                            {
                            "food_name":"Hamburger",
                            "quantity":"4"
                            },
                            {
                            "food_name":"pizza",
                            "quantity":"9"
                            }
                           ]
            }
        ]



#ORDER STATUS UPDATE INPUT FOR TESTS

sample_order_updates=[
                {
                "completed_status":"true",
                "accepted_status":"true"
                },
                {
                "completed_status":"true",
                "accepted_status":"true"
                },
                {
                "completed_status":"",
                "accepted_status":"true"
                },
                {
                "completed_status":"",
                "accepted_status":""
                },
                {
                "completed_status":"",
                "accepted_status":"true"
                },
                {
                "completed_status":"true",
                "accepted_status":""
                },
                {
                "completed_status":"true",
                "accepted_status":"true"
                }
            ]


sample_user=[
            {
            "name":"maryn",
            "email":"maryn@gmail.com",
            "username":"kiki",
            "password":"pass",
            "password2":"pass"
            },
            {
            "email":"maryn@gmail.com",  
            "password":"pass"
            },
            {
            "email":"muthuri@gmail.com",    
            "password":"pass"
            }
            ]



'''-------------------------------------------------------------------------------------------------------------------------------'''

#FIXTURES


@pytest.fixture
def user_reg():
    result = app.test_client()
    response = result.post('/api/v1/register', data = json.dumps(sample_user[0]), content_type = 'application/json')
    stat = json.loads(response.data.decode('utf-8'))
    return stat

@pytest.fixture
def user(user_reg):
    result = app.test_client()
    response = result.post('/api/v1/login', data = json.dumps(sample_user[1]), content_type = 'application/json')
    stat2 = json.loads(response.data.decode('utf-8'))
    return stat2

@pytest.fixture
def user_admin():
    result = app.test_client()
    response = result.post('/api/v1/login', data = json.dumps(sample_user[2]), content_type = 'application/json')
    stat2 = json.loads(response.data.decode('utf-8'))
    return stat2



@pytest.fixture
def credentials(user):
    return [('Authentication', user.get_auth_token())]

@pytest.fixture
def credentials_admin():
    return [('Authentication', user_admin.get_auth_token())]


'''-------------------------------------------------------------------------------------------------------------------------------'''

#GET ALL ORDERS TESTS

@pytest.mark.usefixtures('user_admin')
def test_orders_retrive_all(user_admin):
    result=app.test_client()
    response= result.get('/api/v1/orders',content_type='application/json', headers=user_admin)
    assert(response.status_code==404)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#PLACE ORDER TESTS


def test_orders_quantity_not_digit():
    result=app.test_client()
    response= result.post('/api/v1/place_order', data=json.dumps(sample_order[0]) ,content_type='application/json')
    assert(response.status_code==400)

def test_orders_food_name_not_str():
    result=app.test_client()
    response= result.post('/api/v1/place_order', data=json.dumps(sample_order[1]) ,content_type='application/json')
    assert(response.status_code==400)

def test_orders_food_name_empty():
    result=app.test_client()
    response= result.post('/api/v1/place_order', data=json.dumps(sample_order[2]) ,content_type='application/json')
    assert(response.status_code==406)

def test_orders_quantity_empty():
    result=app.test_client()
    response= result.post('/api/v1/place_order', data=json.dumps(sample_order[3]) ,content_type='application/json')
    assert(response.status_code==406)

def test_orders_destination_empty():
    result=app.test_client()
    response= result.post('/api/v1/place_order', data=json.dumps(sample_order[4]) ,content_type='application/json')
    assert(response.status_code==406)

def test_orders_payment_method_empty():
    result=app.test_client()
    response= result.post('/api/v1/place_order', data=json.dumps(sample_order[5]) ,content_type='application/json')
    assert(response.status_code==406)

def test_orders_order_items_empty():
    result=app.test_client()
    response= result.post('/api/v1/place_order', data=json.dumps(sample_order[6]) ,content_type='application/json')
    assert(response.status_code==406)

def test_orders_successfully():
    result=app.test_client()
    response= result.post('/api/v1/place_order', data=json.dumps(sample_order[7]) ,content_type='application/json')
    json.loads(response.data)
    assert(response.status_code==201)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#GET SPECIFIC ORDER TESTS


def test_get_order_negative_identifier():
    result=app.test_client()
    response= result.get('/api/v1/orders/-1' ,content_type='application/json')
    assert(response.status_code == 404)


def test_get_order_not_created():
    result=app.test_client()
    response= result.get('/api/v1/orders/100' ,content_type='application/json')
    assert(response.status_code == 404)

def test_get_order_successfully():
    result=app.test_client()
    response= result.get('/api/v1/orders/1' ,content_type='application/json')
    assert(response.status_code == 200)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#UPDATE AN ORDER STATUS TESTS

#FIND ORDER TESTS

def test_update_order_status_order_nonexistent():
    result=app.test_client()
    response= result.put('/api/v1/orders/100', data=sample_order_updates[0] ,content_type='application/json')
    assert(response.status_code==404)

#UPDATE AN ACCEPTED STATUS TESTS

def test_update_order_status_both_completed_and_accepted():
    result=app.test_client()
    response= result.put('/api/v1/orders/1', data=sample_order_updates[1] ,content_type='application/json')
    assert(response.status_code==403)

def test_update_order_status_completed_before_accepted():
    result=app.test_client()
    response= result.put('/api/v1/orders/1', data=sample_order_updates[2] ,content_type='application/json')
    assert(response.status_code==403)

def test_update_order_status_both_completed_and_accepted_empty():
    result=app.test_client()
    response= result.put('/api/v1/orders/1', data=sample_order_updates[3] ,content_type='application/json')
    assert(response.status_code==403)

def test_update_order_status_accepted_successfully():
    result=app.test_client()
    response= result.put('/api/v1/orders/1', data=json.dumps(sample_order_updates[4]) ,content_type='application/json')
    assert(response.status_code==200)

def test_update_order_status_completed_successfully():
    result=app.test_client()
    response= result.put('/api/v1/orders/1', data=json.dumps(sample_order_updates[5]) ,content_type='application/json')
    assert(response.status_code==200)