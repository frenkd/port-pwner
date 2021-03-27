import shelve
import os
import sys
import socket
import datetime
from datetime import datetime
from servicer import check_output, get_service_name

TARGET = "192.168.1.34"


def scan(target=TARGET):
    db = shelve.open(get_path(target))
    try:
        status = {}
        # scan ports
        for port in range(1, 65535):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)

            result = s.connect_ex((target, port))
            if result == 0:
                print(f"found {port} open ")
                s.sendall("\n".encode())
                try:
                    status[port] = s.recv(4096).decode("utf-8")
                    print(status[port])
                except socket.error:
                    status[port] = None
                    print("no response from server")
                service_id, version = check_output(status[port])
                status[port] = {"version": version, "serviceID": service_id,
                                "service": get_service_name(service_id), "response": status[port], "new": False}
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
                status[port]["updated"] = port_history[port]

        removed_ports = [port for port in ports_old if port not in ports_new]
        for port in removed_ports:
            print(f"Removed {port}, {port_history[port]['version']}")
            status[port] = {"removed": True}

        new_ports = [port for port in ports_new if port not in ports_old]
        for port in new_ports:
            print(f"Added {port}, {status[port]['version']}")
            status[port]["new"] = True

        now_ts = datetime.now().timestamp()
        db[str(now_ts)] = status
        db["last"] = status
        return status

    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
    finally:
        db.close()


def get_last(target=TARGET):
    return shelve.open(get_path(target))["last"]


def get_scans(target=TARGET):
    return list(shelve.open(get_path(target)).keys())


def get_scan(timestamp, target=TARGET):
    return shelve.open(get_path(target))[timestamp]


def get_path(target=TARGET) -> str:
    return "data/"+target
 

if __name__ == "__main__":
    print(get_last())
    print(get_scan('1616870681.286603'))
