from flask import json
import pytest

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
            "email":"mwirigi@gmail.com",	
            "password":"pass"
            }
            ]


sample_food = [
               {"name":"Hamburger", "price":"200",	"image":"image"},
               {"name":"pizza", "price":"200",	"image":"image"},
               {"name":"Burger", "price":"200",	"image":"image"}
              ]

def sign_up_sign_in_helper(test_client):
    '''
    this is a helper function for an ordinary user's registration and login.
    '''
    sign_up = test_client.post('/api/v1/register', data = json.dumps(sample_user[0]), content_type = 'application/json')
    assert (sign_up.status_code == 201)
    sign_in = test_client.post('/api/v1/login', data = json.dumps(sample_user[1]), content_type = 'application/json')
    assert (sign_in.status_code == 200)

def sign_in_helper(test_client):
    '''
    this is a helper function for an ordinary user's login.
    '''
    sign_in = test_client.post('/api/v1/login', data = json.dumps(sample_user[1]), content_type = 'application/json')
    assert (sign_in.status_code == 200)
    
def sign_in_admin_helper(test_client):
    '''
    this is a helper function for an admin user's login.
    '''
    sign_in = test_client.post('/api/v1/login', data = json.dumps(sample_user[2]), content_type = 'application/json')
    assert (sign_in.status_code == 200)


def add_food_helper(test_client):
    '''
    this is a helper function for an admin user's login.
    '''
    sign_in_admin_helper(test_client)
    add_food = test_client.post('/api/v1/add_food', data=json.dumps(sample_food[0]) ,content_type='application/json')
    assert (add_food.status_code == 201)
    add_food = test_client.post('/api/v1/add_food', data=json.dumps(sample_food[1]) ,content_type='application/json')
    assert (add_food.status_code == 201)
    add_food = test_client.post('/api/v1/add_food', data=json.dumps(sample_food[2]) ,content_type='application/json')
    assert (add_food.status_code == 201)



