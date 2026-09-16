const http = require('http');

const PORT = process.env.PORT || 3000;
let isShuttingDown = false;

const server = http.createServer((req, res) => {
  // If receiving a shutdown signal, reject new requests with 503
  if (isShuttingDown) {
    res.writeHead(503, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'Service Unavailable', message: 'Shutting down...' }));
  }

  // Health check endpoint for container orchestrators
  if (req.url === '/healthz' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'healthy', uptime: process.uptime() }));
  }

  // Application root endpoint
  if (req.url === '/' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({
      message: 'SRE Production Container Runtime Active',
      timestamp: new Date().toISOString(),
      pid: process.pid
    }));
  }

  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Not Found' }));
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`[INFO] Server listening on port ${PORT}`);
});

// POSIX Signal Handling for Graceful Shutdown
function gracefulShutdown(signal) {
  console.log(`[WARN] Received ${signal}. Starting graceful shutdown...`);
  isShuttingDown = true;

  // Stop accepting new connections and finish active ones
  server.close(() => {
    console.log('[INFO] Closed all active HTTP connections. Process exiting cleanly.');
    process.exit(0);
  });

  // Force exit if connections take longer than 10 seconds to close
  setTimeout(() => {
    console.error('[ERROR] Forcefully shutting down due to timeout.');
    process.exit(1);
  }, 10000);
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
