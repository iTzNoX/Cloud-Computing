import requests
import importlib.util
import sys
import os

def download_and_import_module(url, module_name, module_path='/app'):
    response = requests.get(url)
    if response.status_code == 200:
        module_code = response.text
        module_file_path = os.path.join(module_path, f'{module_name}.py')
        with open(module_file_path, 'w') as file:
            file.write(module_code)

        spec = importlib.util.spec_from_file_location(module_name, module_file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module
    else:
        raise Exception(f"Failed to download {module_name}.py from {url}")

# URL des Datenbank-Microservice, der json_database.py hostet
json_database_url = "http://container2:8000/json_database.py"
download_and_import_module(json_database_url, "json_database")

import dungeons

if __name__ == "__main__":
    # runs the bot
    dungeons.on_ready()

# JOIN Link: https://discord.com/oauth2/authorize?client_id=1247927018579038278&permissions=8&scope=bot
# Token = MTI0NzkyNzAxODU3OTAzODI3OA.G6W59m.a6JMkmBHooSvt56u7PNJQRe8R7tLRhWXedpYs0
