from flask import Flask , render_template , request , url_for , redirect 
from collections import defaultdict 
import os  
from flask_jwt_extended import create_access_token , jwt_required , JWTManager , get_jwt_identity
from flask import jsonify

# Configuring Flask App 
app = Flask(__name__)

# Configuring JWT 
jwt = JWTManager(app)

# require because we are using jwt without secret key jwt will not work
app.config['SECRET_KEY'] = os.urandom(24) 

def home():
    return render_template('home.html')

def login():
    username = 'ndk'
    password = 'ndk'
    
    if request.method == 'POST':
        response = request.get_json()
        if response and username == response.get('username') and password == response.get('password'):
            
            # Creating a jwt token with algorithm HS256 
            token = create_access_token(identity=username)
            
            # return jsonift because js expects a json response 
            return jsonify( {'access_token' : token , 'message' : 'Login Successfull' } )
        else:
            return jsonify( {'message' : 'Invalid Credentials'} )
    
    # if the request is not a post request then render the home page
    return render_template('home.html' , user_login = None)

@jwt_required() # automatically check if the token is valid
def dashboard():
    token = request.headers.get("Authorization")  # get the token from the header 
    return jsonify( {'message' : 'U r authenticated' , 'token' : token} )


# adding url rules for the routes
app.add_url_rule('/' , endpoint = 'Home' , view_func = home)
app.add_url_rule('/login' , endpoint = 'Login' , view_func = login , methods=['POST','GET'])
app.add_url_rule('/dashboard',endpoint='Dashboard',view_func=dashboard , methods=['GET'])

# running the app
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)