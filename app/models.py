from datetime import datetime,timedelta
from .... import createapp
from ....database import init_db



class ordermodel():
#encapsulates the functions of the order model

    def __init__(self,user_id,cost,decription,status='0):
        self.db = init_db()
        self.user = user_id
        self.cost = cost
        self.description = description
        self.status = status
    def save_order():
        query = """INSERT INTO orders(user_id,cost,decription,status)
        {}{}{}{}

    