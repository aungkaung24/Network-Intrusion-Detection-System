from scapy.all import sniff, IP, TCP, UDP
from collections import defaultdict
import time

# Store packet counts for each IP
packet_count = defaultdict(int)

# Track when the current monitoring window started
start_time = time.time()

# Alert threshold
THRESHOLD = 100


def packet_callback(packet):

    global start_time

    if IP in packet:

        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        # Count packets from each source IP
        packet_count[source_ip] += 1

        print("\n---------------------------")
        print("New Packet Detected")
        print("---------------------------")

        print("Source IP:", source_ip)
        print("Destination IP:", destination_ip)

        if TCP in packet:
            print("Protocol: TCP")
            print("Source Port:", packet[TCP].sport)
            print("Destination Port:", packet[TCP].dport)

        elif UDP in packet:
            print("Protocol: UDP")
            print("Source Port:", packet[UDP].sport)
            print("Destination Port:", packet[UDP].dport)

        else:
            print("Protocol: Other")

    # Check whether one second has passed
    current_time = time.time()

    if current_time - start_time >= 1:

        # Check packet counts for every source IP
        for ip, count in packet_count.items():

            if count > THRESHOLD:

                print("\n================================")
                print("SECURITY ALERT")
                print("================================")
                print("Suspicious High Network Traffic!")
                print("Source IP:", ip)
                print("Packets:", count)
                print("Status: SUSPICIOUS")
                print("================================\n")

        # Reset counts for the next second
        packet_count.clear()
        start_time = current_time


print("Network Intrusion Detection System")
print("Starting network monitoring...")
print("Press CTRL + C to stop.")

sniff(prn=packet_callback, store=False)