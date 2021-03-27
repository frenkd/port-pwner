import shelve
import os
import sys
import socket
import datetime
from datetime import datetime
from servicer import check_output, get_service_name


def scan(target):
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
                                "service": get_service_name(service_id), "response": status[port]}
            s.close()

        print("Scan complete")

        # prepare output
        out = status.copy()
        out["old"] = []
        out["updated"] = []
        out["new"] = []

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
                out["updated"].append(
                    {"old": port_history[port], "new": status[port]})

        removed_ports = [port for port in ports_old if port not in ports_new]
        for port in removed_ports:
            print(f"Removed {port}, {port_history[port]['version']}")
            out["old"].append(port_history[port])

        new_ports = [port for port in ports_new if port not in ports_old]
        for port in new_ports:
            print(f"Added {port}, {status[port]['version']}")
            out["new"].append(status[port])

        now_ts = datetime.now().timestamp()
        db[str(now_ts)] = status
        db["last"] = status
        return out

    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
    finally:
        db.close()


def get_last(target):
    return shelve.open(get_path(target))["last"]


def get_path(target: str) -> str:
    return "data/"+target


if __name__ == "__main__":
    print(scan())
