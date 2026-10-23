import sqlite3
from datetime import datetime

# Name of our database
DATABASE_NAME = "security_alerts.db"


# Create database and table
def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            source_ip TEXT NOT NULL,
            destination_ip TEXT,
            details TEXT,
            severity TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    print("Database initialized successfully!")


# Insert a new security alert
def insert_alert(alert_type, source_ip, destination_ip, details, severity):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO alerts (
            timestamp,
            alert_type,
            source_ip,
            destination_ip,
            details,
            severity
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        alert_type,
        source_ip,
        destination_ip,
        details,
        severity
    ))

    connection.commit()
    connection.close()

    print("Security alert saved to database!")


# Retrieve security alerts
def view_alerts():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM alerts ORDER BY id DESC")

    alerts = cursor.fetchall()

    connection.close()

    return alerts


# Run only when database.py is executed directly
if __name__ == "__main__":
    create_database()