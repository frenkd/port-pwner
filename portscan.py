import pyfiglet
import shelve
import os
import sys
import socket
import datetime
from socket import getservbyport
from datetime import datetime
from compare_versions import check_output

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

        result = s.connect_ex((target, port))
        if result == 0:
            print(f"found {port} open ")
            s.sendall("haha lmao\n".encode())
            try:
                status[port] = s.recv(4096).decode("utf-8")
                print(status[port]) 
            except socket.error:
                status[port] = None
                print("no response from server")
            status[port] = {"version": check_output(
                status[port]), "response": status[port]}
        s.close() 

    print("Scan complete")

    port_history = db.get("last", {})
    ports_old = port_history.keys()
    ports_new = status.keys()

    print(f"old ports: {ports_old}")
    print(f"new ports: {ports_new}")

    unchanged_ports = [port for port in ports_new if port in ports_old]
    for port in unchanged_ports:
        if port_history[port]['version'] != status[port]['version']:
            print(
                f"Service {port_history[port]['version']} changed to {status[port]['version']}")

    removed_ports = [port for port in ports_old if port not in ports_new]
    for port in removed_ports:
        print(f"Removed {port}, {port_history[port]['version']}")
 
    new_ports = [port for port in ports_new if port not in ports_old]
    for port in new_ports:
        print(f"Added {port}, {status[port]['version']}")

    now_ts = datetime.now().timestamp()
    db[str(now_ts)] = status
    db["last"] = status


except KeyboardInterrupt:
    print("\n Exitting Program !!!!")
    sys.exit()
except socket.gaierror:
    print("\n Hostname Could Not Be Resolved !!!!")
    sys.exit()
except socket.error:
    print("\n Server not responding !!!!")
    sys.exit()
finally:
    db.close()
