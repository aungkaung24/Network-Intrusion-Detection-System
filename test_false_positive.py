from scapy.all import IP, TCP
from main import packet_callback
import main
import time

print("======================================")
print("NIDS FALSE POSITIVE TEST")
print("======================================")

# Reset detection state
main.packet_count.clear()
main.port_scan.clear()
main.start_time = time.time()

# TEST 1: Normal traffic
print("\nTEST 1: Normal Network Traffic")

source_ip = "192.168.1.70"
destination_ip = "192.168.1.1"

for i in range(50):
    packet = (
        IP(src=source_ip, dst=destination_ip)
        / TCP(sport=40000 + i, dport=80, flags="A")
    )
    packet_callback(packet)

print("50 normal packets processed.")

# Trigger the one-second evaluation
main.start_time = time.time() - 2

packet = (
    IP(src=source_ip, dst=destination_ip)
    / TCP(sport=50000, dport=80, flags="A")
)

packet_callback(packet)

print("Expected: No HIGH TRAFFIC alert and no PORT SCAN alert")

# TEST 2: Connections to fewer than 5 ports
print("\nTEST 2: Normal TCP Connections")

main.packet_count.clear()
main.port_scan.clear()
main.start_time = time.time()

for port in [80, 443, 8080]:
    packet = (
        IP(src="192.168.1.80", dst="192.168.1.1")
        / TCP(sport=45000, dport=port, flags="S")
    )

    packet_callback(packet)
    print(f"Connection to port {port}")

print("Expected: No PORT SCAN alert")
print("\nFALSE POSITIVE TEST COMPLETED")