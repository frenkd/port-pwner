import shelve
import os
import sys
import socket
import datetime
from datetime import datetime
from servicer import check_output, get_service_name

PORTS_TO_SCAN = [22, 25, 69, 80, 4000, 7777, 25565]  # range(1, 65535)


def scan(target):
    try:
        status = {"target": target}
        # scan ports
        for port in PORTS_TO_SCAN:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)

            result = s.connect_ex((target, port))
            if result == 0:
                print(f"found {port} open ")
                s.sendall("\n".encode())
                try:
                    status[port] = s.recv(4096).decode("utf-8")
                    # print(status[port])
                except socket.error:
                    status[port] = None
                    print("no response from server")
                service_id, version = check_output(status[port])
                status[port] = {"version": version, "serviceID": service_id,
                                "service": get_service_name(service_id), "response": status[port], "new": False}
            s.close()

        db = shelve.open(get_path())
        print("Scan complete")
        if target not in db:
            db[target] = {"last": {}}
        port_history = db[target]["last"]
        ports_old = [k for k in port_history.keys() if isinstance(k, int)]
        ports_new = [k for k in status.keys() if isinstance(k, int)]

        print(f"old ports: {ports_old}")
        print(f"new ports: {ports_new}")

        # TODO check only scanned ports
        unchanged_ports = [port for port in ports_new if port in ports_old]
        for port in unchanged_ports:
            if port_history[port]['version'] != status[port]['version']:
                print(
                    f"Service {port_history[port]['version']} changed to {status[port]['version']}")
                status[port]["updated"] = port_history[port]

        # TODO check only scanned ports
        removed_ports = [port for port in ports_old if port not in ports_new]
        for port in removed_ports:
            print(f"Removed {port}, {port_history[port]['version']}")
            status[port] = {"removed": True}

        # TODO check only scanned ports
        new_ports = [port for port in ports_new if port not in ports_old]
        for port in new_ports:
            print(f"Added {port}, {status[port]['version']}")
            status[port]["new"] = True

        status["summary"] = {"open": len(
            ports_new), "new": len(new_ports)}

        # save current scan and overwrite the latest scan
        now_ts = datetime.now().timestamp()
        x = db[target]
        x[str(now_ts)] = status
        x["last"] = status
        db[target] = x
        return target + "/" + str(now_ts)

    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved")
        sys.exit()
    finally:
        db.close()


def get_last(target):
    db = shelve.open(get_path(), flag='r')
    try:
        if target in db:
            return db[target]["last"]
        return {}
    finally:
        db.close()


def get_scans():
    db = shelve.open(get_path(), flag='r')
    try:
        x = ([{"id": scan, "target": target, "summary": db[target][scan]["summary"]}
              for target in db for scan in db[target] if scan != "last"])
        x.sort(key=lambda x: x["id"], reverse=True)
        return x
    finally:
        db.close()


def get_scans_from_target(target):
    db = shelve.open(get_path(), flag='r')
    try:
        x = ([{"id": scan, "target": target, "summary": db[target][scan]["summary"]}
              for scan in db[target] if scan != "last"])
        x.sort(key=lambda x: x["id"], reverse=True)
        return x
    finally:
        db.close()


def get_scan(timestamp, target):
    return shelve.open(get_path(), flag='r')[target][timestamp]


def get_targets():
    return list(shelve.open(get_path()).keys())


def get_path() -> str:
    return "port_data"


if __name__ == "__main__":
    # print(scan())
    # print(get_last())
    print(get_scans())
    # print(get_targets())
    # print(get_scan('1616876222.176661'))
    # print(get_scans("localhost"))
