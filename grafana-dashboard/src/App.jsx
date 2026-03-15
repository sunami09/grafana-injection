import './App.css'

const GRAFANA_BASE = 'http://localhost:3000/d-solo/demo-monitoring-01/demo-service-monitoring?orgId=1&refresh=5s&from=now-15m&to=now&__feature.dashboardScene=true'

const panels = [
  { id: 'panel-1', title: 'CPU Usage (%)' },
  { id: 'panel-2', title: 'Memory Usage (%)' },
  { id: 'panel-3', title: 'Requests per second' },
  { id: 'panel-4', title: 'Error Rate' },
]

function Panel({ id, title }) {
  return (
    <div className="panel">
      <h3>{title}</h3>
      <iframe
        src={`${GRAFANA_BASE}&panelId=${id}`}
        width="100%"
        height="300"
        frameBorder="0"
      />
    </div>
  )
}

function App() {
  return (
    <div className="app">
      <h1>Service Monitoring</h1>
      <div className="grid">
        {panels.map(p => <Panel key={p.id} {...p} />)}
      </div>
    </div>
  )
}

export default App