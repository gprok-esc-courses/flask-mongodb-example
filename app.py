from flask import Flask
from flask_pymongo import pymongo
import dotenv
import os
import json
from bson.json_util import loads, dumps

dotenv.load_dotenv()
mongo_user = os.getenv('MONGO_ATLAS_USER')
mongo_pass = os.getenv('MONGO_ATLAS_PASSWORD')

app = Flask(__name__)

connection_string = "mongodb+srv://"+mongo_user+":"+mongo_pass+"@cluster0.jnw32.mongodb.net/test"
client = pymongo.MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)
sample_db = client.get_database('sample')
users_collection = pymongo.collection.Collection(sample_db, 'users')


@app.route("/")
def home():
    return "MongoDB example!"

@app.route("/users")
def users():
    data = users_collection.find()
    user_list = []
    for document in data:
        user_list.append({'username':document['username'], 'password':document['password']})
    print(user_list)
    return user_list

@app.route("/add")
def add():
    users_collection.insert_one({"username":"abc", "password": "123"})
    return "User added"

if __name__ == '__main__':
    print(connection_string)
    app.run(port=5001)