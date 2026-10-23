import csv
import os
from datetime import datetime
from database import create_database, insert_alert

LOG_FILE = "security_alerts.csv"


def save_alert(alert_type, source_ip, destination_ip, details):

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists or os.path.getsize(LOG_FILE) == 0:
            writer.writerow([
                "Timestamp",
                "Alert Type",
                "Source IP",
                "Destination IP",
                "Details"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            alert_type,
            source_ip,
            destination_ip,
            details
        ])

    print("Security alert saved to CSV!")
        # Set severity based on alert type
    if alert_type == "PORT_SCAN":
        severity = "MEDIUM"

    elif alert_type == "HIGH_TRAFFIC":
        severity = "LOW"

    else:
        severity = "UNKNOWN"

    # Initialize the database
    create_database()

    # Save the security alert
    insert_alert(
        alert_type,
        source_ip,
        destination_ip,
        details,
        severity
    )