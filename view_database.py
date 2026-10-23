from database import view_alerts

print("\n===== SECURITY ALERT DATABASE =====")

# Get all alerts from SQLite
alerts = view_alerts()

if not alerts:
    print("No security alerts found.")

else:
    for alert in alerts:

        print("\n----------------------------")
        print("Alert ID:", alert[0])
        print("Timestamp:", alert[1])
        print("Alert Type:", alert[2])
        print("Source IP:", alert[3])
        print("Destination IP:", alert[4])
        print("Details:", alert[5])
        print("Severity:", alert[6])

print("\nDatabase check completed!")