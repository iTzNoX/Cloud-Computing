import os
import json

# Create json database
database = {}

def initialize_database(file_name='database.json'):
    # Check if the file exists, if not, create an empty JSON file
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            json.dump({}, f)
        print(f"Created new database file: {file_name}")

def save_database(file_name='database.json'):
    with open(file_name, 'w') as f:
        json.dump(database, f, indent=4)

def load_database(file_name='database.json'):
    global database
    try:
        with open(file_name, 'r') as f:
            database = json.load(f)
    except FileNotFoundError:
        database = {}

def add_data(key, value):
    global database
    database[key] = value
    save_database()
    print(f"Data added: {key} -> {value}")

def remove_data(key):
    global database
    if key in database:
        del database[key]
        save_database()
        print(f"Data with key '{key}' removed.")
    else:
        print(f"Key '{key}' not found.")

def update_data(key, value):
    global database
    if key in database:
        database[key] = value
        save_database()
        print(f"Data updated: {key} -> {value}")
    else:
        print(f"Key '{key}' not found. Use add_data to add new data.")

# Initialize and load the database at the start
initialize_database()
load_database()