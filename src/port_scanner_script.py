import socket
import threading
import sys
from tqdm import tqdm
from queue import Queue
from datetime import datetime

# Input for target details
target = input("Enter the target IP or hostname: ")

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Error: Unable to resolve hostname.")
    sys.exit()

start_port = int(input("Enter the starting port: "))
end_port = int(input("Enter the ending port: "))

# Queue for threading and storing open ports
queue = Queue()
open_ports = []

# Displaying target information
print(f"\nScanning Target: {target_ip}")
print(f"Port Range: {start_port}-{end_port}")
print(f"Starting the scan...\n")

# Initialize tqdm progress bar
progress_bar = tqdm(total=end_port - start_port + 1, desc="Scanning Ports")

def scan_port(port):
    """
    Function to scan a single port
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((target_ip, port)) == 0:
                open_ports.append(port)
    except Exception:
        pass
    finally:
        progress_bar.update(1)  # Update progress bar

def write_file(file_name):
    """
    Function to write open ports to a file
    """
    with open(file_name, 'w') as f:
        f.write(f"Open Ports for {target_ip}:\n")
        for port in open_ports:
            f.write(f"Port {port}: OPEN\n")

def threader():
    """
    Thread worker function
    """
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

# Record start time
start_time = datetime.now()

# Enqueue all ports to the queue
for port in range(start_port, end_port + 1):
    queue.put(port)

# Create and start threads
threads = []
for _ in range(50):  # Adjust thread count as needed
    thread = threading.Thread(target=threader)
    threads.append(thread)
    thread.start()

# Wait for threads to finish
queue.join()

# Close the progress bar
progress_bar.close()

# Record end time
end_time = datetime.now()

# Display scan results
print("\nScan Completed!")
print(f"Open ports: {open_ports}")
print(f"Time taken: {end_time - start_time}")

# Ask to write output to a file
ask_file = input("Do you want to write the output in a file? (Y/N): ")
if ask_file.lower() == 'y':
    file_name = input("Enter file name: ")
    write_file(file_name)
    print(f"Output written to {file_name}")
else:
    print("Exiting...")
