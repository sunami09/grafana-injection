import json, requests

GRAFANA_URL  = 'http://localhost:3000'
GRAFANA_USER = 'admin'
GRAFANA_PASS = 'admin'

def panel(pid, title, expr, x, y, w=12, h=8, unit='short'):
    return {
        "id": pid,
        "title": title,
        "type": "timeseries",
        "gridPos": {"x": x, "y": y, "w": w, "h": h},
        "fieldConfig": {"defaults": {"unit": unit}},
        "targets": [{
            "datasource": {"type": "prometheus"},
            "expr": expr,
            "legendFormat": "{{instance}}",
            "refId": "A"
        }]
    }

dashboard = {
    "uid":   "demo-monitoring-01",
    "title": "Demo Service Monitoring",
    "refresh": "5s",
    "time": {"from": "now-15m", "to": "now"},
    "panels": [
        panel(1, "CPU Usage (%)",       'demo_cpu_percent',       x=0,  y=0,  unit='percent'),
        panel(2, "Memory Usage (%)",    'demo_mem_percent',       x=12, y=0,  unit='percent'),
        panel(3, "Requests per second", 'demo_requests_per_sec',  x=0,  y=8),
        panel(4, "Error Rate",          'demo_error_rate',        x=12, y=8),
    ]
}

resp = requests.post(
    f'{GRAFANA_URL}/api/dashboards/db',
    auth=(GRAFANA_USER, GRAFANA_PASS),
    headers={'Content-Type': 'application/json'},
    data=json.dumps({"dashboard": dashboard, "overwrite": True})
)

print(resp.status_code, resp.json())


'''
inject_dashboard.py talks to Grafana's HTTP API to create a dashboard entirely from code — no clicking in the UI required.
panel() function
A helper that builds one panel's JSON. Every panel in Grafana is just a JSON object, so instead of repeating the same structure 4 times, panel() takes the important bits as arguments:

expr — the PromQL query (what data to show, e.g. demo_cpu_percent)
title — the panel title
x, y — position on the grid (Grafana uses a 24-column grid)
w, h — width and height
unit — how to format the numbers (percent, short, s, etc.)

dashboard dict
The full dashboard model. This is literally what Grafana stores internally — we're just building it in Python instead of clicking. It defines 4 panels in 2 rows:

Row 1 (y=0): CPU and Memory side by side
Row 2 (y=8): Requests per second and Error rate side by side

Each panel points at Prometheus as the datasource and uses {{instance}} as the legend so each of web-1, web-2, web-3 gets its own line automatically.
requests.post
Sends the whole thing to http://localhost:3000/api/dashboards/db with basic auth. Grafana receives it and creates the dashboard instantly. "overwrite": True means you can edit the dashboard dict and re-run the script to update it — it won't create a duplicate.


you always push the full dashboard JSON — you can't push just one panel. So to add a pie chart you would:

Add a new panel to the panels list in the script
Re-run the script
Grafana replaces the whole dashboard with the new version


'''