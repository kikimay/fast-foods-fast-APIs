from app import app
from flask import Flask, request, session, jsonify, make_response
import os



 



if __name__ == "__main__":
app.secret_key = os.urandom(12)
app.run(debug=True)





        