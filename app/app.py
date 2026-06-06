from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Define a counter to track total requests by method, endpoint, and status
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

# Define a histogram to track request latency in seconds
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)


@app.route('/')
def home():
    start_time = time.time()
    response = jsonify({"message": "DevOps Demo App", "status": "running"})
    # Increment the request counter with labels
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=200).inc()
    # Record how long the request took
    REQUEST_LATENCY.labels(method='GET', endpoint='/').observe(time.time() - start_time)
    return response


@app.route('/health')
def health():
    # Kubernetes liveness and readiness probes will hit this endpoint
    return jsonify({"status": "healthy"}), 200


@app.route('/metrics')
def metrics():
    # Return all registered metrics in Prometheus text format
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)