import socket
import ssl
from datetime import datetime
import requests
import pickle

import subprocess
import platform


class Monitor:
    def __init__(self, host, port, type, priority):
        self.host = host
        self.port = port
        self.type = type
        self.priority = priority

        self.history = []
        self.alert = False

    def check_connection(self):
        self.history.append("0")
        msg = ""
        success = False
        now = datetime.now()

        try:
            if self.type == "plain":
                socket.create_connection((self.host, self.port), timeout=15)
                msg = f"{self.host} is online on port {self.port} with {self.type}"
                success = True
                self.alert = False
            elif self.type == "ssl":
                ssl.wrap_socket(
                    socket.create_connection((self.host, self.port), timeout=15)
                )
                msg = f"{self.host} is online on port {self.port} with {self.type}"
                success = True
                self.alert = False
            else:
                if self.ping():
                    msg = f"{self.host} is online on port {self.port} with {self.type}"
                    success = True
                    self.alert = False
        except socket.timeout:
            msg = f"Server {self.host} timed out on port {self.port}"
        except (ConnectionResetError, ConnectionResetError) as e:
            msg = f"Server {self.host} {e}"
        except Exception as e:
            msg = f"Unknown Error: {e}"
        except:
            pass

        self.create_history(msg, success, now)

    def create_history(self, msg, success, now):
        history_max = 100
        self.history.append((msg, success, now))

        while len(self.history) > history_max:
            self.history.pop(0)

    def ping(self):
        try:
            output = subprocess.check_output(
                "ping -{} 1 {}".format(
                    "n" if platform.system().lower() == "windows" else "c", self.host
                ),
                shell=True,
                universal_newlines=True,
            )
            if "unreachable" in output:
                return False
            else:
                return False
        except Exception:
            return False


if __name__ == "__main__":
    servers = []
    with open("servers.txt", "r") as serverfile:
        for server in serverfile:
            servers.append(server)
        for server in servers:
            host, port, conn_type, prio = server.split(",")
            monitor = Monitor(host, port, conn_type, prio)
            monitor.check_connection()
            print(monitor.history[-1])
