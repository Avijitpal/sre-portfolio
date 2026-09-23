const http = require('http');
const client = require('prom-client');

const PORT = process.env.PORT || 3000;

// 1. Create a Prometheus Registry
const register = new client.Registry();

// Enable default runtime metrics (CPU usage, memory heap, event loop lag, etc.)
client.collectDefaultMetrics({ register });

// 2. Define custom metrics for Golden Signals (Traffic, Latency, Errors)
const httpRequestCounter = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests received',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register],
});

const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5], // Latency buckets
  registers: [register],
});

let isShuttingDown = false;

const server = http.createServer(async (req, res) => {
  const start = process.hrtime();

  res.on('finish', () => {
    // Record request metrics after response completes
    const diff = process.hrtime(start);
    const durationInSeconds = diff[0] + diff[1] / 1e9;
    
    // Normalize route to prevent metric explosion
    const route = req.url.split('?')[0];
    const labels = {
      method: req.method,
      route: route,
      status_code: res.statusCode,
    };

    httpRequestCounter.inc(labels);
    httpRequestDuration.observe(labels, durationInSeconds);
  });

  if (isShuttingDown) {
    res.writeHead(503, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'unhealthy', reason: 'shutting down' }));
  }

  // Prometheus scrape endpoint
  if (req.url === '/metrics' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': register.contentType });
    return res.end(await register.metrics());
  }

  // Health probe endpoint
  if (req.url === '/healthz' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'ok', uptime: process.uptime() }));
  }

  // Default API endpoint
  if (req.url === '/' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({
      message: 'SRE Production Service Online',
      version: 'v2-monitored',
      env: process.env.APP_ENV || 'production'
    }));
  }

  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'not found' }));
});

server.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});

function gracefulShutdown(signal) {
  console.log(`Received ${signal}. Starting graceful shutdown...`);
  isShuttingDown = true;

  server.close(() => {
    console.log('HTTP server closed. Exiting cleanly.');
    process.exit(0);
  });

  setTimeout(() => {
    console.error('Forcefully exiting due to timeout');
    process.exit(1);
  }, 10000);
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
