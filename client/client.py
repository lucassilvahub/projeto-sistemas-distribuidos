import zmq
import json
from datetime import datetime

SERVER_ADDR = "tcp://server:5555"  # nome do container do servidor no docker-compose

def send_request(socket, service, data):
    message = {"service": service, "data": data}
    socket.send_json(message)
    reply = socket.recv_json()
    return reply

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(SERVER_ADDR)

    print("Cliente conectado ao servidor.")

    while True:
        print("\nEscolha uma opção:")
        print("1. Login")
        print("2. Listar usuários")
        print("3. Criar canal")
        print("4. Listar canais")
        print("5. Sair")

        choice = input("Opção: ")

        if choice == "1":
            user = input("Digite o nome de usuário: ")
            data = {"user": user, "timestamp": datetime.now().isoformat()}
            response = send_request(socket, "login", data)
            print("Resposta:", json.dumps(response, indent=4, ensure_ascii=False))

        elif choice == "2":
            data = {"timestamp": datetime.now().isoformat()}
            response = send_request(socket, "users", data)
            print("Resposta:", json.dumps(response, indent=4, ensure_ascii=False))

        elif choice == "3":
            channel = input("Digite o nome do canal: ")
            data = {"channel": channel, "timestamp": datetime.now().isoformat()}
            response = send_request(socket, "channel", data)
            print("Resposta:", json.dumps(response, indent=4, ensure_ascii=False))

        elif choice == "4":
            data = {"timestamp": datetime.now().isoformat()}
            response = send_request(socket, "channels", data)
            print("Resposta:", json.dumps(response, indent=4, ensure_ascii=False))

        elif choice == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
