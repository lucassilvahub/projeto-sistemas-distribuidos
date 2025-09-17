import zmq
import json
import os
from datetime import datetime

STORAGE_FILE = "storage.json"

# Inicializa armazenamento
if not os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "w") as f:
        json.dump({"users": [], "channels": []}, f)

def load_storage():
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def save_storage(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def handle_login(data):
    storage = load_storage()
    username = data["user"]
    timestamp = data["timestamp"]

    if username in storage["users"]:
        return {
            "service": "login",
            "data": {
                "status": "erro",
                "timestamp": timestamp,
                "description": f"Usuário '{username}' já existe."
            }
        }

    storage["users"].append(username)
    save_storage(storage)

    return {
        "service": "login",
        "data": {
            "status": "sucesso",
            "timestamp": timestamp
        }
    }

def handle_users(data):
    storage = load_storage()
    return {
        "service": "users",
        "data": {
            "timestamp": data["timestamp"],
            "users": storage["users"]
        }
    }

def handle_channel(data):
    storage = load_storage()
    channel_name = data["channel"]
    timestamp = data["timestamp"]

    if channel_name in storage["channels"]:
        return {
            "service": "channel",
            "data": {
                "status": "erro",
                "timestamp": timestamp,
                "description": f"Canal '{channel_name}' já existe."
            }
        }

    storage["channels"].append(channel_name)
    save_storage(storage)

    return {
        "service": "channel",
        "data": {
            "status": "sucesso",
            "timestamp": timestamp
        }
    }

def handle_channels(data):
    storage = load_storage()
    return {
        "service": "channels",
        "data": {
            "timestamp": data["timestamp"],
            "users": storage["channels"]
        }
    }

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Servidor iniciado na porta 5555...")

    while True:
        message = socket.recv_json()
        service = message.get("service")
        data = message.get("data")

        if service == "login":
            response = handle_login(data)
        elif service == "users":
            response = handle_users(data)
        elif service == "channel":
            response = handle_channel(data)
        elif service == "channels":
            response = handle_channels(data)
        else:
            response = {
                "service": service,
                "data": {
                    "status": "erro",
                    "timestamp": datetime.now().isoformat(),
                    "description": "Serviço desconhecido"
                }
            }

        socket.send_json(response)

if __name__ == "__main__":
    main()
