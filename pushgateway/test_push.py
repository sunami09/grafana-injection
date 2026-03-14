from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()
g = Gauge('test_metric', 'A test metric', registry=registry)
g.set(42)

push_to_gateway('localhost:9091', job='test', registry=registry)
print("Pushed!")