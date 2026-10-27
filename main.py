from scapy.all import sniff, IP, TCP
from collections import defaultdict
from alert_logger import save_alert
import time


# ==========================================
# HIGH TRAFFIC DETECTION
# ==========================================

packet_count = defaultdict(int)

THRESHOLD = 100

# Track time
start_time = time.time()


# ==========================================
# PORT SCAN DETECTION
# ==========================================

port_scan = defaultdict(list)

PORT_THRESHOLD = 5
PORT_WINDOW = 10


# ==========================================
# PACKET CALLBACK FUNCTION
# ==========================================

def packet_callback(packet):

    global start_time

    if IP in packet:

        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        current_time = time.time()

        # Count packets from each source IP
        packet_count[source_ip] += 1

        # ==========================================
        # PORT SCAN DETECTION
        # ==========================================

        if TCP in packet:

            destination_port = packet[TCP].dport

            # Check for TCP SYN without ACK
            flags = packet[TCP].flags

            if flags & 0x02 and not flags & 0x10:

                # Save destination port and timestamp
                port_scan[source_ip].append(
                    (destination_ip, destination_port, current_time)
                )

                # Remove entries older than PORT_WINDOW
                port_scan[source_ip] = [
                    entry
                    for entry in port_scan[source_ip]
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

                    # Save port scan alert
                    save_alert(
                        "PORT_SCAN",
                        source_ip,
                        destination_ip,
                        f"Ports detected: {sorted(unique_ports)}"
                    )

                    # Clear entries for this target
                    # to prevent repeated alerts
                    port_scan[source_ip] = [
                        entry
                        for entry in port_scan[source_ip]
                        if entry[0] != destination_ip
                    ]

    # ==========================================
    # HIGH TRAFFIC DETECTION
    # ==========================================

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
                print("Status: POSSIBLE HIGH TRAFFIC")
                print("==============================\n")

                # Save high traffic alert to CSV and SQLite
                save_alert(
                    "HIGH_TRAFFIC",
                    ip,
                    "MULTIPLE",
                    f"Detected {count} packets in approximately 1 second"
                )

        # Reset packet counts for the next interval
        packet_count.clear()

        # Reset monitoring timer
        start_time = current_time


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("====================================")
    print("Network Intrusion Detection System")
    print("====================================")

    print("Monitoring network traffic...")
    print("High Traffic Threshold:", THRESHOLD)
    print("Port Scan Threshold:", PORT_THRESHOLD)
    print("Port Scan Window:", PORT_WINDOW, "seconds")
    print("Press CTRL + C to stop.")

    sniff(
        prn=packet_callback,
        store=False
    )