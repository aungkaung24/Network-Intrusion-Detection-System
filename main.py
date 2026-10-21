from scapy.all import sniff, IP, TCP, UDP

def packet_callback(packet):

    if IP in packet:

        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

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

print("Network Intrusion Detection System")
print("Starting packet monitoring...")
print("Press CTRL + C to stop.")

sniff(prn=packet_callback, store=False)