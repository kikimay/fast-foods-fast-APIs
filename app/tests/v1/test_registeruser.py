import pytest
from flask import json
from app.views import app
from app.views import Users

testusers = Users()


#REGISTRATION INPUT FOR TESTS

sample_registration = [
{
 "name":"",
 "email":"maryn@gmail.com",
 "username":"delight",
 "password":"delight",
 "password2":"delight"
},
{
 "name":"maryn",
 "email":"",
 "username":"kiki",
 "password":"pass",
 "password2":"pass"
},
{
 "name":"maryn",
 "email":"maryn@gmail.com",
 "username":"",
 "password":"pass",
 "password2":"pass"
},
{
 "name":"maryn",
 "email":"maryn@gmail.com",
 "username":"kiki",
 "password":"",
 "password2":"pass"
},
{
 "name":"maryn",
 "email":"maryn@gmail.com",
 "username":"kiki",
 "password":"pass",
 "password2":""
},
{
 "name":"maryn",
 "email":"maryn@gmailcom",
 "username":"kiki",
 "password":"pass",
 "password2":"pass"
},
{
 "name":"maryn",
 "email":"maryngmail.com",
 "username":"kiki",
 "password":"pass",
 "password2":"pass"
},
{
 "name":"maryn",
 "email":"maryn@gmail.com",
 "username":"kiki",
 "password":"pass",
 "password2":"pass1"
},
{
 "name":"maryn",
 "email":"maryn@gmail.com",
 "username":"kiki",
 "password":"pass11",
 "password2":"pass1"
},
{
 "name":"maryn",
 "email":"maryn@gmail.com",
 "username":"kiki",
 "password":"pass",
 "password2":"pass"
},
{
 "name":"maryn",
 "email":"mary@gmail.com",
 "username":"kiki",
 "password":"pass",
 "password2":"pass"
}
]


#LOGIN CREDENTIALS FOR TESTS

sample_login = [
{
 "email":"", 
 "password":"pass"
},
{
 "email":"maryn@gmail.com",  
 "password":""
},
{
 "email":"maryngmail.com",   
 "password":"pass"
},
{
 "email":"maryn@gmailcom",   
 "password":"pass"
},
{
 "email":"mary@gmail.com",   
 "password":"pass1"
},
{
 "email":"mary@gmail.com",   
 "password":"pass1"
},
{
 "email":"maryn@gmail.com",  
 "password":"pass"
}
]



'''---------------------------------------------------------------------------------------------------------------------'''

#REGISTRATION TESTS

#USER INPUT CHECKS
  
def test_register_empty_name():
    result = app.test_client()
    response = result.post('/api/v1/register', data = sample_registration[0], content_type = 'application/json')
    assert(response.status_code == 400)

def test_register_empty_email():
    result = app.test_client()
    response = result.post('/api/v1/register', data = sample_registration[1], content_type = 'application/json')
    assert(response.status_code == 400)

def test_register_empty_username():
    result = app.test_client()
    response = result.post('/api/v1/register', data = sample_registration[2], content_type = 'application/json')
    assert(response.status_code == 400)

def test_register_empty_password():
    result = app.test_client()
    response = result.post('/api/v1/register', data = sample_registration[3], content_type = 'application/json')
    assert(response.status_code == 400)

def test_register_empty_password2():
    result = app.test_client()
    response = result.post('/api/v1/register', data = sample_registration[4], content_type = 'application/json')
    assert(response.status_code == 400)


#EMAIL FORMAT CHECKS

def test_register_wrong_email_format():
    result = app.test_client()
    response = result.post('/api/v1/register', data = sample_registration[5], content_type = 'application/json')
    assert(response.status_code == 400)

def test_register_wrong_email_format1():
    result = app.test_client()
    response = result.post('/api/v1/register', data = sample_registration[6], content_type = 'application/json')
    assert(response.status_code == 400)


#PASSWORD CHECK

def test_register_passwords_matching():
    result = app.test_client()
    response = result.post('/api/v1/register', data = sample_registration[7], content_type = 'application/json')
    assert(response.status_code == 400)

def test_register_passwords_matching1():
    result = app.test_client()
    response = result.post('/api/v1/register', data = sample_registration[8], content_type = 'application/json')
    assert(response.status_code == 400)


#CORRECT INPUT

def test_register_correct_data():
    result = app.test_client()
    response = result.post('/api/v1/register', data = json.dumps(sample_registration[9]), content_type = 'application/json')
    json.loads(response.data.decode('utf-8'))
    assert (response.status_code == 201)


#DUPLICATE INPUT

def test_register_duplicate_input():
    result = app.test_client()
    response = result.post('/api/v1/register', data = sample_registration[10], content_type = 'application/json')
    assert (response.status_code == 400)

'''---------------------------------------------------------------------------------------------------------------------'''

#LOGIN TESTS

#INPUT CHECKS

    
def test_login_empty_email():
    result = app.test_client()
    response = result.post('/api/v1/login', data = sample_login[0], content_type = 'application/json')
    assert(response.status_code == 400)

def test_login_empty_password():
    result = app.test_client()
    response = result.post('/api/v1/login', data = sample_login[1], content_type = 'application/json')
    assert(response.status_code == 400)

def test_login_wrong_email_format():
    result = app.test_client()
    response = result.post('/api/v1/login', data = sample_login[2], content_type = 'application/json')
    assert(response.status_code == 400)

def test_login_wrong_email_format2():
    result = app.test_client()
    response = result.post('/api/v1/login', data = sample_login[3], content_type = 'application/json')
    assert(response.status_code == 400)


#CREDENTIALS CHECK

def test_login_wrong_password():
    result = app.test_client()
    response = result.post('/api/v1/login', data = sample_login[4], content_type = 'application/json')
    assert(response.status_code == 400)

def test_login_wrong_email():
    result = app.test_client()
    response = result.post('/api/v1/login', data = sample_login[5], content_type = 'application/json')
    assert(response.status_code == 400)


#CORRECT CREDENTIALS

def test_login_correct_data():
    result = app.test_client()
    response = result.post('/api/v1/login', data = json.dumps(sample_login[6]), content_type = 'application/json')
    json.loads(response.data.decode('utf-8'))
    assert(response.status_code == 200)


'''--------------------------------------------------------------------------------------------------------------------------------------'''


#LOGOUT TESTS

def test_logout_correctly():
    result=app.test_client()
    response= result.get('/api/v1/logout', content_type = 'application/json')
    assert(response.status_code == 200)
