import time
from unittest.mock import patch

from scapy.all import IP, TCP
import main


def run_test(name, packets, expected_alert):
    detected_alerts = []

    def capture_alert(alert_type, source_ip, destination_ip, details):
        detected_alerts.append(alert_type)

    # Reset the detector before each test
    main.packet_count.clear()
    main.port_scan.clear()
    main.start_time = time.time()

    with patch.object(main, "save_alert", side_effect=capture_alert):

        for packet in packets:
            main.packet_callback(packet)

        # Trigger the packet-rate evaluation
        main.start_time = time.time() - 2

        main.packet_callback(
            IP(src="192.168.1.254", dst="192.168.1.1")
            / TCP(dport=80, flags="A")
        )

    detected = expected_alert in detected_alerts if expected_alert else bool(detected_alerts)

    if expected_alert:
        passed = detected
    else:
        passed = not detected

    print(f"\n{name}")
    print(f"Expected: {expected_alert or 'NORMAL'}")
    print(f"Detected: {detected_alerts or 'NORMAL'}")
    print(f"Result: {'PASS' if passed else 'FAIL'}")

    return passed, bool(expected_alert), bool(detected_alerts)


def make_packets(count, source_ip):
    return [
        IP(src=source_ip, dst="192.168.1.1")
        / TCP(sport=40000 + i, dport=80, flags="A")
        for i in range(count)
    ]


def make_port_packets(ports, source_ip):
    return [
        IP(src=source_ip, dst="192.168.1.1")
        / TCP(sport=45000, dport=port, flags="S")
        for port in ports
    ]


print("=" * 45)
print("NIDS DETECTION ACCURACY TEST")
print("=" * 45)

results = []

results.append(
    run_test(
        "Test 1: Normal traffic (50 packets)",
        make_packets(50, "192.168.1.70"),
        None
    )
)

results.append(
    run_test(
        "Test 2: High traffic (110 packets)",
        make_packets(110, "192.168.1.60"),
        "HIGH_TRAFFIC"
    )
)

results.append(
    run_test(
        "Test 3: Normal connections (3 ports)",
        make_port_packets([80, 443, 8080], "192.168.1.80"),
        None
    )
)

results.append(
    run_test(
        "Test 4: Port scan (5 ports)",
        make_port_packets([21, 22, 80, 443, 3389], "192.168.1.50"),
        "PORT_SCAN"
    )
)

tp = sum(1 for passed, attack, detected in results if attack and detected)
tn = sum(1 for passed, attack, detected in results if not attack and not detected)
fp = sum(1 for passed, attack, detected in results if not attack and detected)
fn = sum(1 for passed, attack, detected in results if attack and not detected)

total = tp + tn + fp + fn

accuracy = (tp + tn) / total * 100 if total else 0
precision = tp / (tp + fp) * 100 if tp + fp else 0
recall = tp / (tp + fn) * 100 if tp + fn else 0

print("\n" + "=" * 45)
print("DETECTION EVALUATION RESULTS")
print("=" * 45)

print(f"True Positives: {tp}")
print(f"True Negatives: {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")

print(f"\nAccuracy: {accuracy:.2f}%")
print(f"Precision: {precision:.2f}%")
print(f"Recall: {recall:.2f}%")