import requests
import importlib.util
import sys

# handles container requests
#------------------------------------------------------
# URL des Datenbank-Microservice, der json_database.py hostet
url = "http://container2:8000/json_database.py"

# Herunterladen der Datei in den Speicher
response = requests.get(url)
if response.status_code == 200:
    code = response.text
else:
    raise Exception("Failed to download json_database.py")

# Speichern der Datei im temporären Verzeichnis
temp_module_path = '/app/json_database.py'
with open(temp_module_path, 'w') as file:
    file.write(code)

# Laden des Moduls von der temporären Datei
spec = importlib.util.spec_from_file_location("json_database", temp_module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.modules["json_database"] = module
#------------------------------------------------------

import dungeons

if __name__ == "__main__":
    # runs the bot
    dungeons.on_ready()

# JOIN Link: https://discord.com/oauth2/authorize?client_id=1247927018579038278&permissions=8&scope=bot
# Token = MTI0NzkyNzAxODU3OTAzODI3OA.G6W59m.a6JMkmBHooSvt56u7PNJQRe8R7tLRhWXedpYs0
