from flask import Flask

# Load the views

from app import views




# Initialize the app
app = Flask(__name__, instance_relative_config=True)



# Load the config file
app.config.from_object('instance.config')


