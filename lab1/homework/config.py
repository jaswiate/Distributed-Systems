IP = '127.0.0.1'
PORT = 9009
ADDRESS = (IP, PORT)
BUFFER_SIZE = 2048
MAX_CLIENTS = 4

MULTICAST_GROUP = '224.0.0.1'
MULTICAST_PORT = 9008
MULTICAST_ADDRESS = (MULTICAST_GROUP, MULTICAST_PORT)

def rgb(r, g, b):
  return f"\033[38;2;{r};{g};{b}m"

RED = rgb(255, 0, 0)
GREEN = rgb(0, 255, 0)
BLUE = rgb(0, 0, 255)
ORANGE = rgb(255, 69, 0)
CYAN = rgb(0, 255, 255)
YELLOW = rgb(255, 255, 0)
PINK = rgb(255, 20, 147)

R = "\033[0m"

