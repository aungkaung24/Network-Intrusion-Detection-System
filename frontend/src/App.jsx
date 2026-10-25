import { useEffect, useState } from 'react'
import './App.css'
function App() {

  const [statistics, setStatistics] = useState({
    total_alerts: 0,
    port_scan_alerts: 0,
    high_traffic_alerts: 0
  })

  const [connected, setConnected] = useState(false)

  const [recentAlerts, setRecentAlerts] = useState([])

  useEffect(() => {

    async function fetchStatistics() {
      try {
        const response = await fetch(
          'http://127.0.0.1:8000/alerts/statistics'
        )

        if (!response.ok) {
          throw new Error('Failed to fetch statistics')
        }

        const data = await response.json()

        setStatistics(data)
        setConnected(true)

      } catch (error) {
        console.error('Backend connection error:', error)
        setConnected(false)
      }
    }

    fetchStatistics()

    async function fetchRecentAlerts() {
  try {
    const response = await fetch(
      'http://127.0.0.1:8000/alerts/recent'
    )

    if (!response.ok) {
      throw new Error('Failed to fetch recent alerts')
    }

    const data = await response.json()

    setRecentAlerts(data)

  } catch (error) {
    console.error('Error loading recent alerts:', error)
  }
}

fetchRecentAlerts()

  }, [])

  return (
    <div className="dashboard">

      <header className="header">
        <div>
          <h1>🛡️ Network Intrusion Detection System</h1>
          <p>Security Monitoring Dashboard</p>
        </div>

        <span className="status">
  {connected ? '● Backend Connected' : '● Backend Disconnected'}
</span>
      </header>

      <main>
        <section className="stats">

          <div className="card">
            <h3>Total Security Alerts</h3>
            <h2>{statistics.total_alerts}</h2>
            <p>Recorded security events</p>
          </div>

          <div className="card">
            <h3>Port Scan Alerts</h3>
            <h2>{statistics.port_scan_alerts}</h2>
            <p>Potential scanning activity</p>
          </div>

          <div className="card">
            <h3>High Traffic Alerts</h3>
            <h2>{statistics.high_traffic_alerts}</h2>
            <p>Unusual traffic volume</p>
          </div>

        </section>

        <section className="alerts">
          <div className="section-header">
            <h2>🚨 Recent Security Alerts</h2>
            <span>Latest Events</span>
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Timestamp</th>
                  <th>Alert Type</th>
                  <th>Source IP</th>
                  <th>Destination IP</th>
                  <th>Severity</th>
                </tr>
              </thead>

              <tbody>
  {recentAlerts.length === 0 ? (
    <tr>
      <td colSpan="6">No security alerts found.</td>
    </tr>
  ) : (
    recentAlerts.map((alert) => (
      <tr key={alert.id}>
        <td>{alert.id}</td>
        <td>{alert.timestamp}</td>
        <td>{alert.alert_type}</td>
        <td>{alert.source_ip}</td>
        <td>{alert.destination_ip}</td>
        <td>
          <span className={`severity ${alert.severity.toLowerCase()}`}>
            {alert.severity}
          </span>
        </td>
      </tr>
    ))
  )}
</tbody>
            </table>
          </div>
        </section>
      </main>

      <footer>
        Network Intrusion Detection System | Cybersecurity Project
      </footer>

    </div>
  )
}

export default App