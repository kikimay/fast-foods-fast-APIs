from flask import flask
 #initialize app
app =flask(__name__, instance_relative_config=True)
 
 from app import views

#Load the config file
 app.config.from_object('config')
 sss