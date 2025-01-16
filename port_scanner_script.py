import socket
import sys
from datetime import datetime

target=input("Enter the target IP or hostname:")

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Error: Unable to resolve hostname.")
    sys.exit()


#Port range
start_port = int(input("Enter the starting port: "))
end_port = int(input("Enter the ending port: "))

# Display scan details
print(f"\nScanning Target: {target_ip}")
print(f"Port Range: {start_port}-{end_port}")
print(f"Starting the scan...\n")


try:
    # Record the start time
    scan_start = datetime.now()

    #Perform the scan
    for port in range (start_port , end_port+1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1) # time out for connection it is in seconds in this case 1
            #try connection to the port
            result = s.connect_ex((target_ip, port))
            
            if result == 0:
                print (f"Port {port}: OPEN ")

            s.close()

    scan_end = datetime.now()

    duration = scan_end - scan_start
    print (f"\nScan completed in {duration}.")
except KeyboardInterrupt:
    print("\nScan abort by user.")
    sys.exit()
except socket.error:
    print("Error: Unable to connect to the network.")
    sys.exit()

