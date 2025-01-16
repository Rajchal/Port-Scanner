import socket
import threading
import sys
from queue import Queue
from datetime import datetime

target=input("Enter the target IP or hostname:")

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Error: Unable to resolve hostname.")
    sys.exit()


start_port = int(input("Enter the starting port: "))
end_port = int(input("Enter the ending port: "))

queue = Queue()

open_ports = []

print(f"\nScanning Target: {target_ip}")
print(f"Port Range: {start_port}-{end_port}")
print(f"Starting the scan...\n")

def scan_port (port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((target_ip, port)) == 0:
                print(f"Port {port}:OPEN")
                open_ports.append(port)
    except Exception:
        pass

def threader():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

start_time = datetime.now()

for port in range(start_port, end_port + 1):
    queue.put(port)

threads=[]

for _ in range(50):
    thread = threading.Thread(target=threader)
    threads.append(thread)
    thread.start()

queue.join()

end_time = datetime.now()


print ("\nScan Completed!")
print (f"Open ports: {open_ports}")
print (f"Time taken: {end_time - start_time}")



