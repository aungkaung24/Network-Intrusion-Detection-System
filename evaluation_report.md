# Network Intrusion Detection System
## Detection Evaluation Report

**Generated:** 2026-10-28 10:13:43

## 1. Project Overview

This project implements a Python-based Network Intrusion Detection
System (NIDS) using Scapy, SQLite, FastAPI, and React.

The system monitors network packets and generates alerts for:

- Potential port scanning
- Unusually high network traffic

## 2. Detection Thresholds

| Detection Type | Threshold |
|---|---|
| High Traffic | More than 100 packets per second |
| Port Scan | 5 unique destination TCP ports within 10 seconds |

## 3. Initial Detection Evaluation

| Metric | Result |
|---|---|
| True Positives | 2 |
| True Negatives | 2 |
| False Positives | 0 |
| False Negatives | 0 |
| Accuracy | 100% |
| Precision | 100% |
| Recall | 100% |

These results are based on four controlled simulated test cases.

## 4. Advanced Detection Testing

| Test | Expected Result | Status |
|---|---|---|
| 99 packets | No alert | PASS |
| 100 packets | No alert | PASS |
| 101 packets | HIGH_TRAFFIC | PASS |
| 4 destination TCP ports | No alert | PASS |
| 5 destination TCP ports | PORT_SCAN | PASS |
| Repeated connections to one port | No alert | PASS |

**Advanced testing result: 6/6 passed.**

## 5. Limitations

- Tests use simulated Scapy packets.
- Real-world attack detection accuracy has not been measured.
- High packet volume does not necessarily indicate an attack.
- Legitimate services may connect to multiple destination ports.
- Detection thresholds are currently fixed.
- The system does not yet use machine learning.

## 6. Conclusion

The NIDS passed all ten controlled test cases across the
initial and advanced evaluations.

The results demonstrate correct threshold-based detection
under the tested conditions.

Future improvements include larger labelled datasets,
real-world traffic evaluation, and machine learning-based
anomaly detection.
