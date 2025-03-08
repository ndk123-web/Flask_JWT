from flask import Flask , render_template , request , url_for , redirect 
from collections import defaultdict 
import os  
from flask_jwt_extended import create_access_token , jwt_required , JWTManager , get_jwt_identity , create_refresh_token
from flask import jsonify

# Configuring Flask App 
app = Flask(__name__)

# Configuring JWT 
jwt = JWTManager(app)

# require because we are using jwt without secret key jwt will not work
app.config['SECRET_KEY'] = os.urandom(24) 
app.config['JWT_SECRET_KEY'] = os.urandom(24)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 300 # 5 minutes
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400  # 1 day


# home route
def home():
    return render_template('home.html')


# login route
def login():
    username = 'ndk'
    password = 'ndk'
    
    if request.method == 'POST':
        response = request.get_json()
        if response and username == response.get('username') and password == response.get('password'):
            
            # Creating a jwt token with algorithm HS256 
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            # return jsonift because js expects a json response 
            return jsonify( {'access_token' : access_token , 'refresh_token' : refresh_token , 'message' : 'Login Successfull' } )
        else:
            return jsonify( {'message' : 'Invalid Credentials'} )
    
    # if the request is not a post request then render the home page
    return render_template('home.html' , user_login = None)


# dashboard route
@jwt_required() # automatically check if the token is valid
def dashboard():
    token = request.headers.get("Authorization")  # get the token from the header 
    return jsonify( {'message' : 'U r authenticated' , 'token' : token} )


# refresh route
# means if token expire then it will not return 401 error , it will return 200 status code and runs the refresh function 
@jwt_required(refresh=True)  # ← Requires REFRESH token in header
def refresh():
    # Gets identity from the REFRESH token's payload
    current_user = get_jwt_identity() 
    
    # Creates new ACCESS token with same identity
    new_access_token = create_access_token(identity=current_user)
    return jsonify( {'access_token' : new_access_token , 'message' : 'Tokenn refreshed' } )  # return the new access token


# adding url rules for the routes
app.add_url_rule('/' , endpoint = 'Home' , view_func = home)
app.add_url_rule('/login' , endpoint = 'Login' , view_func = login , methods=['POST','GET'])
app.add_url_rule('/dashboard',endpoint='Dashboard',view_func=dashboard , methods=['GET'])
app.add_url_rule('/refresh' , endpoint = 'Refresh' , view_func=refresh , methods=['POST'])

# running the app
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)