from fastapi import FastAPI
from database import view_alerts
from fastapi.middleware.cors import CORSMiddleware
# Create FastAPI application
app = FastAPI(
    title="Network Intrusion Detection System",
    description="Cybersecurity monitoring API",
    version="1.0.0"
)

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"]
)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Network Intrusion Detection System API",
        "status": "running"
    }


# Get all security alerts
@app.get("/alerts")
def get_alerts():

    alerts = view_alerts()
    results = []

    for alert in alerts:
        results.append({
            "id": alert[0],
            "timestamp": alert[1],
            "alert_type": alert[2],
            "source_ip": alert[3],
            "destination_ip": alert[4],
            "details": alert[5],
            "severity": alert[6]
        })
@app.get("/alerts/recent")
def get_recent_alerts():

    alerts = view_alerts()

    recent_alerts = alerts[:5]

    results = []

    for alert in recent_alerts:
        results.append({
            "id": alert[0],
            "timestamp": alert[1],
            "alert_type": alert[2],
            "source_ip": alert[3],
            "destination_ip": alert[4],
            "details": alert[5],
            "severity": alert[6]
        })

    return results

# Get security alert statistics
@app.get("/alerts/statistics")
def get_statistics():

    # Retrieve alerts from database
    alerts = view_alerts()

    # Count total alerts
    total_alerts = len(alerts)

    port_scan_count = 0
    high_traffic_count = 0

    # Count each alert type
    for alert in alerts:

        alert_type = alert[2]

        if alert_type == "PORT_SCAN":
            port_scan_count += 1

        elif alert_type == "HIGH_TRAFFIC":
            high_traffic_count += 1

    # Return statistics
    return {
        "total_alerts": total_alerts,
        "port_scan_alerts": port_scan_count,
        "high_traffic_alerts": high_traffic_count
    }
# Security severity statistics
@app.get("/alerts/severity")
def get_severity_statistics():

    alerts = view_alerts()

    low_count = 0
    medium_count = 0
    high_count = 0

    for alert in alerts:

        severity = alert[6]

        if severity == "LOW":
            low_count += 1

        elif severity == "MEDIUM":
            medium_count += 1

        elif severity == "HIGH":
            high_count += 1

    return {
        "low": low_count,
        "medium": medium_count,
        "high": high_count
    }

    