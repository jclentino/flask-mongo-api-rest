from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util  
from bson.objectid import ObjectId  

app = Flask(__name__)
app.config['MONGO_URI'] = 'strin de conexion'
mongo = PyMongo(app)


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()   
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json') 

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if username and password and email:
        hashedPassword = generate_password_hash(password)
        id = mongo.db.users.insert_one({    
            'username': username,
            'email': email,
            'password': hashedPassword
        })

        response = {
            'username': username,
            'email': email,
            'password': hashedPassword
        }

        return response 
    else:
        return not_found()

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({ '_id': ObjectId(id) })
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json') 

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    deleted = mongo.db.users.delete_one({ '_id': ObjectId(id) })
    response = jsonify({ 'msg': 'deleted successfully'})
    return response

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    hashedPassword = generate_password_hash(password)
    id = mongo.db.users.update_one(
        { '_id': ObjectId(id) },
        {
            '$set': {
                'username': username,
                'email': email,
                'password': hashedPassword
            }
        }
    )
    response = jsonify({ 'message': "user update successfully"})
    return response 


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource not found ' + request.url,
        'status': 404
    })
    response.status_code = 404

    return response

if __name__ == "__main__":
    app.run(debug=True)
    print("Conexión a la base de datos:", mongo.cx)

