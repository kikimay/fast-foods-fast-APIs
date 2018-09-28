from flask import Flask
# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the views


from app.api.v2 import foods
from app.api.v2 import orders
from app.api.v2 import users
from app.api.v2.database import DatabaseConnection, conn, cur, save



# Load the config file
app.config.from_object('config')
