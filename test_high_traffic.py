from scapy.all import IP, TCP
from main import packet_callback, packet_count
import main
import time


print("====================================")
print("Starting High Traffic Detection Test")
print("====================================")

# Clear previous packet counts
packet_count.clear()

# Reset monitoring timer
main.start_time = time.time()

# Simulate 110 packets from the same IP
for i in range(110):

    packet = IP(
        src="192.168.1.60",
        dst="192.168.1.103"
    ) / TCP(
        sport=50000,
        dport=80,
        flags="A"
    )

    packet_callback(packet)

print("\n110 simulated packets processed.")

# Wait for the monitoring interval to finish
time.sleep(1.1)

# Trigger the packet count check
packet_callback(
    IP(
        src="192.168.1.60",
        dst="192.168.1.103"
    ) / TCP(
        sport=50000,
        dport=80,
        flags="A"
    )
)

print("\nHigh Traffic Detection Test Completed!")