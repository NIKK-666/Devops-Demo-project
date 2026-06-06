from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import os

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)


@app.route('/')
def home():
    start_time = time.time()

    response = jsonify({
        "message": "DevOps Demo App",
        "status": "running"
    })

    REQUEST_COUNT.labels(
        method='GET',
        endpoint='/',
        status='200'
    ).inc()

    REQUEST_LATENCY.labels(
        method='GET',
        endpoint='/'
    ).observe(time.time() - start_time)

    return response


@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200


@app.route('/metrics')
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
