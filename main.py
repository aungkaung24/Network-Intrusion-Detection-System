from scapy.all import sniff, IP, TCP
from collections import defaultdict
import time

# High traffic detection
packet_count = defaultdict(int)

THRESHOLD = 100

# Port scan detection
port_scan = defaultdict(list)

PORT_THRESHOLD = 5
PORT_WINDOW = 10

# Track time
start_time = time.time()


def packet_callback(packet):

    global start_time

    if IP in packet:

        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        current_time = time.time()

        # Count packets
        packet_count[source_ip] += 1

        # PORT SCAN DETECTION
        if TCP in packet:

            destination_port = packet[TCP].dport

            # Check for TCP SYN without ACK
            flags = packet[TCP].flags

            if flags & 0x02 and not flags & 0x10:

                # Save destination port and time
                port_scan[source_ip].append(
                    (destination_ip, destination_port, current_time)
                )

                # Remove entries older than 10 seconds
                port_scan[source_ip] = [
                    entry for entry in port_scan[source_ip]
                    if current_time - entry[2] <= PORT_WINDOW
                ]

                # Count unique destination ports
                unique_ports = {
                    entry[1]
                    for entry in port_scan[source_ip]
                    if entry[0] == destination_ip
                }

                if len(unique_ports) >= PORT_THRESHOLD:

                    print("\n==============================")
                    print("PORT SCAN ALERT!")
                    print("==============================")
                    print("Source IP:", source_ip)
                    print("Target IP:", destination_ip)
                    print("Ports Detected:", sorted(unique_ports))
                    print("Status: POSSIBLE PORT SCAN")
                    print("==============================\n")

                    # Clear entries for this target to avoid repeated alerts
                    port_scan[source_ip] = [
                        entry for entry in port_scan[source_ip]
                        if entry[0] != destination_ip
                    ]

    # HIGH TRAFFIC DETECTION
    current_time = time.time()

    if current_time - start_time >= 1:

        print("\n===== PACKET COUNT =====")

        for ip, count in packet_count.items():

            print("IP:", ip, "| Packets:", count)

            if count > THRESHOLD:

                print("\n==============================")
                print("HIGH TRAFFIC ALERT!")
                print("==============================")
                print("Source IP:", ip)
                print("Packets:", count)
                print("==============================\n")

        packet_count.clear()
        start_time = current_time


if __name__ == "__main__":

    print("Network Intrusion Detection System")
    print("Monitoring network traffic...")
    print("Press CTRL + C to stop.")

    sniff(prn=packet_callback, store=False)