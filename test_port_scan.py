from scapy.all import IP, TCP
from main import packet_callback

# Simulated attacker IP
source_ip = "192.168.1.50"

# Simulated target IP
destination_ip = "192.168.1.103"

# Ports to test
ports = [21, 22, 80, 443, 3389]

print("Starting Port Scan Detection Test")
print("---------------------------------")

for port in ports:

    # Create a simulated TCP SYN packet
    packet = IP(
        src=source_ip,
        dst=destination_ip
    ) / TCP(
        sport=50000,
        dport=port,
        flags="S"
    )

    print("Testing Port:", port)

    # Send packet directly to our detection function
    packet_callback(packet)

print("\nTest Completed!")