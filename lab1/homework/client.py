import socket
import struct
from threading import Thread
import config


def receive_TCP(tcp_socket):
    while True:
        data = tcp_socket.recv(config.BUFFER_SIZE)
        if not data:
            break
        print(f"{config.BLUE}{data.decode()}{config.R}")

def send_TCP(tcp_socket, message):
    tcp_socket.send(message.encode())

def receive_UDP(udp_socket):
    while True:
        data, _ = udp_socket.recvfrom(config.BUFFER_SIZE)
        print(f"{config.ORANGE}{data.decode()}{config.R}")

def send_UDP(udp_socket):
    with open('ascii_art.txt', 'r') as file:
        media_data = file.read()
    udp_socket.sendto(media_data.encode(), config.ADDRESS)

def receive_MCAST(mcast_socket):
    while True:
        data, _ = mcast_socket.recvfrom(config.BUFFER_SIZE)
        print(f"{config.CYAN}{data.decode()}{config.R}")

def send_MCAST(mcast_socket):
    with open('ascii_art.txt', 'r') as file:
        media_data = file.read()
    mcast_socket.sendto(media_data.encode(), config.MULTICAST_ADDRESS)


tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(config.ADDRESS)
_, tcp_port = tcp_socket.getsockname()

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('', tcp_port))

mcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
mcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mcast_socket.bind(('', config.MULTICAST_PORT))

group = socket.inet_aton(config.MULTICAST_GROUP)
mcast_socket.setsockopt(
    socket.IPPROTO_IP, 
    socket.IP_ADD_MEMBERSHIP, 
    struct.pack('4sL', group, socket.INADDR_ANY)
)

client_name = input("Enter your nickname: ")
tcp_socket.send(client_name.encode())

receive_thread_TCP = Thread(
    target=receive_TCP, 
    args=(tcp_socket,)
)
receive_thread_TCP.start()

receive_thread_UDP = Thread(
    target=receive_UDP, 
    args=(udp_socket,)
)
receive_thread_UDP.start()

receive_thread_MCAST = Thread(
    target=receive_MCAST,
    args=(mcast_socket,)
)
receive_thread_MCAST.start()

while True:
    try:
        message = input()
    except KeyboardInterrupt:
        tcp_socket.close()
        udp_socket.close()
        raise SystemExit
    if not message:
        continue

    data = f"{client_name}: {message}"

    if message in ['u', 'U']:
        send_UDP(udp_socket)
    elif message in ['m', 'M']:
        send_MCAST(mcast_socket)
    else:
        send_TCP(tcp_socket, message)

