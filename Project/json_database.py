from flask import Flask, request
import os
import json

app = Flask(__name__)

# Pfad zur JSON-Datenbankdatei
database_file = 'database.json'
# check for database.json, if not exists create empty
if not os.path.exists(database_file):
    with open(database_file, 'w') as f:
        json.dump({}, f)
# Pfad zur JSON-Datenbankdatei
database_file = 'database.json'

@app.route('/database', methods=['GET'])
def get_database():
    # loads database
    with open(database_file, 'r') as f:
        database = json.load(f)
    return database

@app.route('/database', methods=['POST',  'PUT', 'GET'])
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


@app.route('/database/<key>', methods=['PUT'])
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


@app.route('/database/<key>', methods=['DELETE'])
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
    app.run(host='0.0.0.0', port=8000)
