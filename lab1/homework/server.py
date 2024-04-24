import socket
from threading import Thread
import config

clients = {}

def handle_client_TCP(client_socket, client_address):
    client_name = client_socket.recv(config.BUFFER_SIZE).decode()
    clients[client_address] = (client_socket, client_name)
    print(f"{config.RED}{client_name} joined the chat!{config.R}")

    while True:
        data = client_socket.recv(config.BUFFER_SIZE)
        if not data: 
            break
        message = data.decode()

        for client in clients.values():
            if client[0] != client_socket:
                client[0].send(f"{client_name}: {message}".encode())

    client_socket.close()
    del clients[client_address]
        
def handle_client_UDP(udp_socket):
    while True:
        data, udp_address = udp_socket.recvfrom(config.BUFFER_SIZE)
        client_name = clients.get(addr, "Unknown")[1]
        print(f"{config.PINK}{client_name}{config.R}")

        for client in clients.keys():
            if client != udp_address:
                udp_socket.sendto(data, client)


tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_socket.bind(config.ADDRESS)
tcp_socket.listen(5)

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
udp_socket.bind(config.ADDRESS)

print(f"{config.GREEN}Server listening on {config.ADDRESS} (TCP) (UDP){config.R}")

udp_thread = Thread(
    target=handle_client_UDP,
    args=(udp_socket,),
    daemon=True
)
udp_thread.start()

while True:
    client_socket, addr = tcp_socket.accept()
    client_thread = Thread(
        target=handle_client_TCP, 
        args=(client_socket, addr)
    )
    client_thread.start()

