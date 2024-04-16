"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
Jhon = {
    "id": jackson_family._generateId(),
    "name":"John Jackson",
    "age": "33 Years old",
    "lucky_numbers": [7, 13, 22]
}

jackson_family.add_member(Jhon)

Jane = {
    "id": jackson_family._generateId(),
    "name":"Jane Jackson",
    "age":"35 Years old",
    "lucky_numbers": [10, 14, 3]
}

jackson_family.add_member(Jane)

Jimmy = {
    "id": jackson_family._generateId(),
    "name": "Jimmy  Jackson",
    "age": "5 Years old",
    "lucky_numbers": 1
}

jackson_family.add_member(Jimmy)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

#creando endpoint post
@app.route('/member', methods=['POST'])
def add_member():  
     new_member = request.json
     success = jackson_family.add_member(new_member)
     if success == True: 
         return jsonify(new_member), 200
     return jsonify(success), 400

#creando endpoint delete
@app.route('/member/<int:member_id>', methods=["DELETE"])
def delete_member(member_id):
    success = jackson_family.delete_member(member_id)
    return jsonify({'done': True}), 200
      
    #buscar un solo miembro
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    one_member = jackson_family.get_member(member_id)
    return jsonify(one_member), 200
    
    # this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
