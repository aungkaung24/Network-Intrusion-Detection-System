import { useEffect, useState } from 'react'

import {
  BarChart,
  Bar,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts'

import './App.css'

function App() {

  // Security statistics
  const [statistics, setStatistics] = useState({
    total_alerts: 0,
    port_scan_alerts: 0,
    high_traffic_alerts: 0
  })

  // Backend connection status
  const [connected, setConnected] = useState(false)

  // Recent security alerts
  const [recentAlerts, setRecentAlerts] = useState([])

  // Security severity statistics
  const [severityStats, setSeverityStats] = useState({
    low: 0,
    medium: 0,
    high: 0
  })

  // Alert filter
  const [alertFilter, setAlertFilter] = useState('ALL')

  // Security alert chart data
  const chartData = [
    {
      name: 'Port Scan',
      alerts: statistics.port_scan_alerts
    },
    {
      name: 'High Traffic',
      alerts: statistics.high_traffic_alerts
    }
  ]

  // Security severity chart data
  const severityChartData = [
    {
      name: 'LOW',
      alerts: severityStats.low,
      fill: '#22c55e'
    },
    {
      name: 'MEDIUM',
      alerts: severityStats.medium,
      fill: '#f59e0b'
    },
    {
      name: 'HIGH',
      alerts: severityStats.high,
      fill: '#ef4444'
    }
  ]

  // Filter security alerts
  const filteredAlerts = recentAlerts.filter((alert) => {

    if (alertFilter === 'ALL') {
      return true
    }

    return alert.alert_type === alertFilter
  })

  // Fetch data from FastAPI
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

    async function fetchSeverityStats() {

      try {

        const response = await fetch(
          'http://127.0.0.1:8000/alerts/severity'
        )

        if (!response.ok) {
          throw new Error('Failed to fetch severity statistics')
        }

        const data = await response.json()

        setSeverityStats(data)

      } catch (error) {

        console.error('Error loading severity statistics:', error)

      }
    }

    // Fetch immediately when dashboard loads
    fetchStatistics()
    fetchRecentAlerts()
    fetchSeverityStats()

    // Refresh every 5 seconds
    const interval = setInterval(() => {

      fetchStatistics()
      fetchRecentAlerts()
      fetchSeverityStats()

    }, 5000)

    // Stop refresh when component unmounts
    return () => clearInterval(interval)

  }, [])

  return (

    <div className="dashboard">

      {/* Dashboard Header */}

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

        {/* Security Statistics */}

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

        {/* Security Alert Statistics Chart */}

        <section className="chart-section">

          <div className="section-header">

            <h2>📊 Security Alert Statistics</h2>

            <span>Alert Distribution</span>

          </div>

          <div className="chart-container">

            <ResponsiveContainer width="100%" height="100%">

              <BarChart data={chartData}>

                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#334155"
                />

                <XAxis
                  dataKey="name"
                  stroke="#94a3b8"
                />

                <YAxis
                  stroke="#94a3b8"
                  allowDecimals={false}
                />

                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: '1px solid #334155',
                    color: '#ffffff'
                  }}
                />

                <Bar
                  dataKey="alerts"
                  fill="#38bdf8"
                  radius={[6, 6, 0, 0]}
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </section>

        {/* Security Severity Analysis Chart */}

        <section className="chart-section">

          <div className="section-header">

            <h2>🛡️ Security Severity Analysis</h2>

            <span>Severity Distribution</span>

          </div>

          <div className="chart-container">

            <ResponsiveContainer width="100%" height="100%">

              <BarChart data={severityChartData}>

                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#334155"
                />

                <XAxis
                  dataKey="name"
                  stroke="#94a3b8"
                />

                <YAxis
                  stroke="#94a3b8"
                  allowDecimals={false}
                />

                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: '1px solid #334155',
                    color: '#ffffff'
                  }}
                />

                <Bar
                  dataKey="alerts"
                  radius={[6, 6, 0, 0]}
                >
                  {severityChartData.map((entry) => (
                    <Cell
                      key={entry.name}
                      fill={entry.fill}
                    />
                  ))}
                </Bar>

              </BarChart>

            </ResponsiveContainer>

          </div>

        </section>

        {/* Recent Security Alerts */}

        <section className="alerts">

          <div className="section-header">

            <h2>🚨 Recent Security Alerts</h2>

            {/* Alert Filter */}

            <select
              className="alert-filter"
              value={alertFilter}
              onChange={(event) => setAlertFilter(event.target.value)}
            >

              <option value="ALL">
                All Alerts
              </option>

              <option value="PORT_SCAN">
                Port Scan
              </option>

              <option value="HIGH_TRAFFIC">
                High Traffic
              </option>

            </select>

          </div>

          {/* Security Alerts Table */}

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

                {filteredAlerts.length === 0 ? (

                  <tr>
                    <td colSpan="6">
                      No security alerts found.
                    </td>
                  </tr>

                ) : (

                  filteredAlerts.map((alert) => (

                    <tr key={alert.id}>

                      <td>{alert.id}</td>

                      <td>{alert.timestamp}</td>

                      <td>{alert.alert_type}</td>

                      <td>{alert.source_ip}</td>

                      <td>{alert.destination_ip}</td>

                      <td>

                        <span
                          className={`severity ${String(alert.severity || 'UNKNOWN').toLowerCase()}`}
                        >
                          {alert.severity || 'UNKNOWN'}
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

      {/* Footer */}

      <footer>

        Network Intrusion Detection System | Cybersecurity Project

      </footer>

    </div>

  )
}

export default App