import time
from unittest.mock import patch

from scapy.all import IP, TCP
import main


def reset_detector():
    main.packet_count.clear()
    main.port_scan.clear()
    main.start_time = time.time()


def test_traffic(packet_total, expected_alert):
    reset_detector()
    detected_alerts = []

    def capture_alert(alert_type, source_ip, destination_ip, details):
        detected_alerts.append(alert_type)

    with patch.object(main, "save_alert", side_effect=capture_alert):

        for i in range(packet_total):
            packet = (
                IP(src="192.168.1.60", dst="192.168.1.1")
                / TCP(sport=40000 + i, dport=80, flags="A")
            )
            main.packet_callback(packet)

        # Force the packet-rate evaluation without adding another packet.
        main.start_time = time.time() - 2

        main.packet_callback(
            IP(src="192.168.1.254", dst="192.168.1.1")
            / TCP(dport=80, flags="A")
        )

    detected = "HIGH_TRAFFIC" in detected_alerts
    passed = detected == expected_alert

    return passed, detected_alerts


def test_ports(ports, expected_alert):
    reset_detector()
    detected_alerts = []

    def capture_alert(alert_type, source_ip, destination_ip, details):
        detected_alerts.append(alert_type)

    with patch.object(main, "save_alert", side_effect=capture_alert):

        for port in ports:
            packet = (
                IP(src="192.168.1.50", dst="192.168.1.1")
                / TCP(sport=45000, dport=port, flags="S")
            )
            main.packet_callback(packet)

    detected = "PORT_SCAN" in detected_alerts
    passed = detected == expected_alert

    return passed, detected_alerts


print("=" * 45)
print("NIDS ADVANCED DETECTION TEST")
print("=" * 45)

tests = [
    ("99 packets", test_traffic(99, False)),
    ("100 packets", test_traffic(100, False)),
    ("101 packets", test_traffic(101, True)),
    ("4 TCP ports", test_ports([21, 22, 80, 443], False)),
    ("5 TCP ports", test_ports([21, 22, 80, 443, 3389], True)),
    ("Repeated same port", test_ports([80] * 10, False)),
]

passed_count = 0

for name, (passed, alerts) in tests:
    status = "PASS" if passed else "FAIL"

    if passed:
        passed_count += 1

    print(f"\nTest: {name}")
    print(f"Detected alerts: {alerts or 'None'}")
    print(f"Result: {status}")

print("\n" + "=" * 45)
print("ADVANCED TEST SUMMARY")
print("=" * 45)
print(f"Passed: {passed_count}/{len(tests)}")
print(f"Failed: {len(tests) - passed_count}")