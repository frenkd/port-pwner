import pyfiglet
import shelve
import os
import sys
import socket
import datetime
from socket import getservbyport
from datetime import datetime

ascii_banner = pyfiglet.figlet_format("port-pwner")
print(ascii_banner)

# Defining a target
if len(sys.argv) == 2:

    # translate hostname to IPv4
    target = socket.gethostbyname(sys.argv[1])
else:
    print("Invalid ammount of Argument")

db = shelve.open('port_data')

# Add Banner
print("-" * 50)
print("Scanning Target: " + target)
print("Scanning started at:" + str(datetime.now()))
print("-" * 50)

try:
    status = {}
    # will scan ports between 1 to 65,535
    for port in range(1, 65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        # returns an error indicator
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"found {port} open ")
            s.sendall("haha lmao\n".encode())
            status[port] = s.recv(4096)
            print(status[port].decode("utf-8"))
        s.close() 

        now_ts = datetime.now().timestamp()
        port_history = db.get("last", {})
        # for port_old, _ in port_history:

        db[now_ts] = status
        db["last"] = status


except KeyboardInterrupt:
    print("\n Exitting Program !!!!")
    sys.exit()
except socket.gaierror:
    print("\n Hostname Could Not Be Resolved !!!!")
    sys.exit()
except socket.error:
    print("\ Server not responding !!!!")
    sys.exit()
finally:
    db.close()
