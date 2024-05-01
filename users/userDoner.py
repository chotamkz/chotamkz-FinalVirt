from flask import Flask, request, jsonify
from supabase import create_client, Client
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600 
jwt = JWTManager(app)


SUPABASE_URL="https://ldenrcqttxxnhernzyph.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxkZW5yY3F0dHh4bmhlcm56eXBoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI4NTI1NTcsImV4cCI6MjAyODQyODU1N30.WCkmIB1k2l2Syap8jo6-vRvH1mLqI8rJhfFqSobFUmY"
SECRET_KEY="cloudcomputing"
app.config['SECRET_KEY']=SECRET_KEY
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def authenticate_user(email, password):
    response, count = supabase.table('Users').select("*").eq('Email', email).execute()

    if 'error' in response:
            error_message = response['error']['message']
            return jsonify({'message': f'Failed to authenticate user: {error_message}'}), 500

    if response[1] == []:
        return None 
    

    user = response[1][0]
    if user['Password'] == password:
        return user 

    return None

@app.route('/test', methods=['POST'])
def test():
    return jsonify(request.get_json())

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('Email')
    password = generate_password_hash(data.get('Password'))

    try:
        existing_user, count = supabase.table('Users').select('*').eq('Email', email).execute()

        if 'error' in existing_user:
            error_message = existing_user['error']['message']
            return jsonify({'message': f'Failed to check existing user: {error_message}'}), 500

        if existing_user[1] != []:
            return jsonify({'message': 'User with the same email already exists'}), 409
        

        response, count = supabase.table('Users').insert([data]).execute()


        if 'error' in response:
            error_message = response['error']['message']
            return jsonify({'message': f'Failed to register user: {error_message}'}), 500

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        return jsonify({'message': f'Failed to register user: {str(e)}'}), 500


@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    email = data['Email']
    password = data['Password']

    try:
        user = authenticate_user(email, password)
        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401
        
        jwt_payload = {
            'Name': user['Name'],
            'is_admin': user['is_admin']
        }


        access_token = create_access_token(identity=user['Email'], additional_claims=jwt_payload)

        return jsonify({'message':"User logged in successfully",'access_token': access_token}), 200

    except Exception as e:
            return jsonify({'message': f'Failed to login user: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
