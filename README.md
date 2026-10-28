# 🛡️ Network Intrusion Detection System (NIDS)

A Python-based Network Intrusion Detection System designed to monitor network traffic, identify suspicious activities, record security alerts, and visualize detection results through a web-based dashboard.

This project demonstrates practical cybersecurity concepts, including packet analysis, intrusion detection, security event logging, backend API development, and security monitoring.

## 📌 Project Overview

The Network Intrusion Detection System (NIDS) monitors network packets using Python and Scapy.

The system identifies two types of potentially suspicious network activities:

* **Port Scanning:** Detects attempts to access multiple TCP ports on a target device within a specified period.
* **High Network Traffic:** Detects unusually high packet volumes originating from an individual IP address.

When suspicious activity is detected, the system generates an alert and stores the event in CSV and SQLite formats.

A React dashboard displays security statistics, alert severity, and recent security events.

## 🚀 Features

### 1. Network Packet Monitoring

* Captures network packets using Scapy.
* Extracts source and destination IP addresses.
* Analyzes TCP connection attempts.
* Tracks packet counts for individual source IP addresses.

### 2. Port Scan Detection

* Monitors TCP SYN packets.
* Tracks unique destination ports.
* Detects potential scanning activity involving five or more unique ports within a 10-second window.
* Generates security alerts when the detection threshold is reached.

### 3. High Traffic Detection

* Counts packets received from individual source IP addresses.
* Detects traffic exceeding 100 packets within an approximately one-second monitoring interval.
* Records suspicious traffic events for further investigation.

### 4. Security Alert Logging

* Stores alerts in CSV format.
* Records security events in a SQLite database.
* Maintains timestamps, alert types, IP addresses, descriptions, and severity levels.

### 5. REST API

Developed using FastAPI.

The API provides access to:

* Security alerts
* Recent security events
* Alert statistics
* Severity statistics

### 6. Security Monitoring Dashboard

Developed using React and Recharts.

Dashboard features include:

* Backend connection status
* Total security alerts
* Port scan statistics
* High traffic statistics
* Security alert distribution charts
* Severity analysis charts
* Recent security alerts table
* Alert filtering
* Automatic data refresh

## 🛠️ Technologies Used

| Technology | Purpose                             |
| ---------- | ----------------------------------- |
| Python     | Intrusion detection logic           |
| Scapy      | Network packet capture and analysis |
| FastAPI    | Backend REST API                    |
| SQLite     | Security alert database             |
| CSV        | Security event logging              |
| React      | Frontend dashboard                  |
| Vite       | Frontend development environment    |
| Recharts   | Security statistics visualization   |
| Git        | Version control                     |
| GitHub     | Source code hosting                 |

## 🏗️ System Architecture

```text
                  Network Traffic
                        |
                        v
                Scapy Packet Capture
                        |
                        v
                Detection Engine
                        |
             +----------+----------+
             |                     |
             v                     v
       Port Scan Detection   High Traffic Detection
             |                     |
             +----------+----------+
                        |
                        v
                 Security Alerts
                        |
             +----------+----------+
             |                     |
             v                     v
          CSV Logs           SQLite Database
                                   |
                                   v
                              FastAPI API
                                   |
                                   v
                            React Dashboard
                                   |
                                   v
                         Security Visualization
```

## 📂 Project Structure

```text
Network-Intrusion-Detection-System/
│
├── main.py
├── alert_logger.py
├── database.py
├── api.py
├── view_database.py
│
├── test_port_scan.py
├── test_high_traffic.py
├── test_false_positive.py
├── test_advanced_detection.py
│
├── generate_evaluation_report.py
├── evaluation_report.md
│
├── requirements.txt
├── README.md
├── .gitignore
│
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── App.css
    │   └── main.jsx
    │
    ├── package.json
    └── vite.config.js
```

## ⚙️ Installation

### Prerequisites

Install the following software:

* Python 3
* Node.js and npm
* Git
* Npcap (required for packet capture on Windows)

### 1. Clone the Repository

```bash
git clone https://github.com/aungkaung24/Network-Intrusion-Detection-System.git
```

Navigate into the project directory:

```bash
cd Network-Intrusion-Detection-System
```

### 2. Create a Python Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```cmd
.venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Backend

```bash
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

The FastAPI backend runs at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

### 5. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local address displayed by Vite to access the dashboard.

### 6. Run Network Monitoring

Open another terminal in the project directory.

Activate the Python virtual environment and execute:

```bash
python main.py
```

Packet capture may require administrator privileges.

## 🧪 Testing and Evaluation

The project includes simulated network traffic tests to evaluate intrusion detection behavior.

### Detection Tests

| Test Scenario                         | Expected Result       |
| ------------------------------------- | --------------------- |
| 99 packets                            | No high traffic alert |
| 100 packets                           | No high traffic alert |
| 101 packets                           | High traffic alert    |
| 4 unique TCP ports                    | No port scan alert    |
| 5 unique TCP ports                    | Port scan alert       |
| Repeated connections to the same port | No port scan alert    |

### Advanced Testing Results

The advanced detection test suite completed successfully:

* Tests executed: 6
* Tests passed: 6
* Tests failed: 0

An additional controlled evaluation reported:

* True Positives: 2
* True Negatives: 2
* False Positives: 0
* False Negatives: 0
* Accuracy: 100%
* Precision: 100%
* Recall: 100%

**Important:** These results apply only to the small, controlled simulation scenarios used during testing. They do not establish equivalent performance against real-world attacks or production network traffic.

See `evaluation_report.md` for additional evaluation information.

## 🔐 Security Alert Severity

The system currently uses basic severity classifications:

| Alert Type   | Severity |
| ------------ | -------- |
| High Traffic | LOW      |
| Port Scan    | MEDIUM   |

These severity levels are initial classifications and do not represent a comprehensive risk assessment.

## ⚠️ Current Limitations

* Detection is based on predefined thresholds.
* Legitimate traffic may occasionally trigger alerts.
* Sophisticated or slow port scans may bypass detection.
* The system does not currently classify attacks using machine learning.
* The application is designed for educational and experimental use.
* Detection accuracy has not been validated against a large real-world intrusion dataset.

## 🔮 Future Improvements

Potential enhancements include:

* Machine learning-based anomaly detection
* Additional intrusion detection rules
* More detailed traffic analysis
* Historical traffic visualization
* Email notifications for security alerts
* Configurable detection thresholds
* Improved false-positive reduction
* Authentication and access control for the dashboard
* Testing with established cybersecurity datasets

## 🎯 Project Objectives

This project was developed to strengthen practical knowledge of:

* Network security
* Intrusion detection
* Python programming
* Network packet analysis
* Database integration
* REST API development
* Frontend development
* Cybersecurity testing and evaluation

## 📜 License

See the `LICENSE` file for licensing information.

## 👨‍💻 Author

**aungkaung24**

GitHub: [aungkaung24](https://github.com/aungkaung24)

---

**Disclaimer:** This project is intended for educational purposes and authorized network security monitoring only.
