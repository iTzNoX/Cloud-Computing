from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

# Pfad zur JSON-Datenbankdatei
database_file = 'database.json'

# Überprüfen, ob die Datenbankdatei vorhanden ist, und ggf. eine leere Datenbank erstellen
if not os.path.exists(database_file):
    with open(database_file, 'w') as f:
        json.dump({}, f)

# Routen für die CRUD-Operationen auf der Datenbank

@app.route('/database', methods=['GET'])
def get_database():
    # Lade die Datenbank
    with open(database_file, 'r') as f:
        database = json.load(f)
    return jsonify(database)

@app.route('/database/<key>', methods=['GET'])
def get_data(key):
    # Lade die Datenbank
    with open(database_file, 'r') as f:
        database = json.load(f)
    # Rückgabe der Daten für den angegebenen Schlüssel
    return jsonify({key: database.get(key, 'Key not found')})

@app.route('/database', methods=['POST'])
def add_data():
    # Lese die Daten aus der Anfrage
    data = request.json
    key = data.get('key')
    value = data.get('value')
    # Lade die Datenbank
    with open(database_file, 'r') as f:
        database = json.load(f)
    # Füge neue Daten hinzu
    database[key] = value
    # Speichere die aktualisierte Datenbank
    with open(database_file, 'w') as f:
        json.dump(database, f, indent=4)
    return jsonify({'message': 'Data added successfully'})

@app.route('/database/<key>', methods=['PUT'])
def update_data(key):
    # Lese die Daten aus der Anfrage
    data = request.json
    value = data.get('value')
    # Lade die Datenbank
    with open(database_file, 'r') as f:
        database = json.load(f)
    # Aktualisiere die Daten für den angegebenen Schlüssel
    database[key] = value
    # Speichere die aktualisierte Datenbank
    with open(database_file, 'w') as f:
        json.dump(database, f, indent=4)
    return jsonify({'message': 'Data updated successfully'})

@app.route('/database/<key>', methods=['DELETE'])
def remove_data(key):
    # Lade die Datenbank
    with open(database_file, 'r') as f:
        database = json.load(f)
    # Überprüfe, ob der Schlüssel vorhanden ist
    if key in database:
        del database[key]
        # Speichere die aktualisierte Datenbank
        with open(database_file, 'w') as f:
            json.dump(database, f, indent=4)
        return jsonify({'message': f'Data with key {key} removed successfully'})
    else:
        return jsonify({'message': f'Key {key} not found'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
