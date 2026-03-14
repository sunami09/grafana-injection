'''
- 3 fake web servers — web-1, web-2, web-3
- Every 5 seconds it pushes 4 metrics for each one:

    demo_cpu_percent — CPU usage, oscillates between ~20-60%
    demo_mem_percent — memory usage, slowly waves between ~50-70%
    demo_error_rate — error rate, random noise around 1%
    demo_requests_per_sec — request rate, waves between ~60-140 req/s


- Each instance is slightly out of phase so they don't all move together — looks more realistic
    math.sin(t / 30 + offset)::: 
    So all three are running the same wave, just shifted. If web-1 is at the peak of its CPU spike, web-2 is somewhere in the middle, and web-3 is still climbing. They never all spike at the same time.
    
- math.sin creates the wave pattern, random adds noise on top
'''


import time, math, random
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

PUSHGATEWAY = 'localhost:9091'
INSTANCES = ['web-1', 'web-2', 'web-3']

def make_metrics(registry, instance):
    cpu = Gauge('demo_cpu_percent', 'CPU usage', ['instance'], registry=registry)
    mem = Gauge('demo_mem_percent', 'Memory usage', ['instance'], registry=registry)
    err = Gauge('demo_error_rate', 'Error rate', ['instance'], registry=registry)
    req = Gauge('demo_requests_per_sec', 'Request rate', ['instance'], registry=registry)
    return cpu, mem, err, req

t = 0
while True:
    for instance in INSTANCES:
        registry = CollectorRegistry()
        cpu, mem, err, req = make_metrics(registry, instance)

        offset = INSTANCES.index(instance) * 20
        cpu.labels(instance=instance).set(40 + 20 * math.sin(t / 30 + offset) + random.uniform(-3, 3))
        mem.labels(instance=instance).set(60 + 10 * math.sin(t / 60 + offset) + random.uniform(-2, 2))
        err.labels(instance=instance).set(max(0, 1 + random.gauss(0, 0.5)))
        req.labels(instance=instance).set(max(0, 100 + 40 * math.sin(t / 20 + offset) + random.uniform(-5, 5)))

        push_to_gateway(PUSHGATEWAY, job='demo', grouping_key={'instance': instance}, registry=registry)

    print(f"Pushed tick {t}")
    t += 1
    time.sleep(5)