from flask import Flask, request
import os
import json
import requests

app = Flask(__name__)

json_database_url = "http://cloudcomputing-container2-1:8000/app/json_database.py"
# Pfad zur JSON-Datenbankdatei
database_file = 'database.json'
# check for database.json, if not exists create empty
if not os.path.exists(database_file):
    with open(database_file, 'w') as f:
        json.dump({}, f)
# Pfad zur JSON-Datenbankdatei
database_file = 'database.json'

@app.route('/', methods=['GET'])
def index():
    return 'Hello, World!'

def get_database():
    try:
        response = requests.get(json_database_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get database. Status code: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error while getting database: {str(e)}")
        return {}

@app.route('/database/getdb', methods=['GET'])
def get_database_route():
    # Database vom lokalen Filesystem laden
    with open(database_file, 'r') as f:
        local_database = json.load(f)
    # Database vom Datenbank-Microservice abrufen
    remote_database = get_database()
    # Merge local und remote Database
    merged_database = {**local_database, **remote_database}
    return merged_database

@app.route('/database', methods=['POST'])
def add_data():
    if request.method == "POST":
        data = request.json
        # takes info and adds data
        key = data["user"]
        value = {
            "user_id": data["user_id"],
            "user_discriminator": data["user_discriminator"],
            "nickname": data["nickname"],
            "avatar": data["avatar"],
            "roles": data["roles"],
            "joined_at": data["joined_at"],
            "created_at": data["created_at"]
        }
        database = get_database()
        database[key] = value

        # saves new database
        with open(database_file, 'w') as f:
            json.dump(database, f, indent=4)
        return 'Data added successfully'
    else:
        return 'Invalid request method'


@app.route('/database/updatedb', methods=['PUT'])
def update_data(givenkey, givenvalue):
    # takes info and updates it
    value = givenvalue
    database = get_database()
    if givenvalue in database:
        database[givenkey] = value

        # saves new database
        with open(database_file, 'w') as f:
            json.dump(database, f, indent=4)
        return 'Data updated successfully'
    else:
        return 'Value not found'


@app.route('/database/rmvdb', methods=['DELETE'])
def remove_data(key):
    # loads and dels database
    database = get_database()
    if key in database:
        del database[key]

        # saves new database
        with open(database_file, 'w') as f:
            json.dump(database, f, indent=4)
        return f'Data with key {key} removed successfully'
    else:
        return f'Key {key} not found'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
