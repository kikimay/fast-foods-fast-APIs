from app.api.v2.models import UserModels

def add_admin_user(self):
    ''' add admin user to the users table'''

    admin = dict(name = "maryn", email = "mwirigi@gmail.com", username = "kiki", password = "kiki", admin = True)

    UserModels.add_users(admin)


    """{
        "admin":True,
        "email":"mwirigi@gmail.com",
        "name":"maryn",
        "password":"pass",
        "user_id":1,
        "username":"kiki"
    }"""