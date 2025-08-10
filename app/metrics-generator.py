import http.server
import socketserver
import threading
import time
import random
import math
import urllib.request

# Port for the HTTP server
PORT = 8000

# CPU-intensive task function
def cpu_intensive_task(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        # Perform some math operations to burn CPU
        for _ in range(100000):
            math.sqrt(random.random())  # Random math to simulate work

# HTTP request handler with some CPU work per request
class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Simulate some work per request (e.g., 0.1-1 second of CPU)
        work_duration = random.uniform(0.1, 1.0)
        cpu_intensive_task(work_duration)
        
        # Send response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Test App</title></head>")
        self.wfile.write(b"<body><p>Request processed.</p></body></html>")

# Function to start the HTTP server in a thread
def start_http_server():
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print(f"HTTP server running on port {PORT}")
        httpd.serve_forever()

# Function for random CPU spikes (independent of HTTP)
def cpu_spike_thread():
    while True:
        # Wait a random time between spikes (10-300 seconds)
        sleep_time = random.uniform(10, 300)
        time.sleep(sleep_time)
        
        # Spike duration (5-60 seconds)
        spike_duration = random.uniform(5, 60)
        print(f"Starting CPU spike for {spike_duration:.2f} seconds")
        cpu_intensive_task(spike_duration)

# Function for random HTTP request spikes
def http_spike_thread():
    while True:
        # Wait a random time between spikes (10-300 seconds)
        sleep_time = random.uniform(10, 300)
        time.sleep(sleep_time)
        
        # Number of requests to send in burst (1-100)
        num_requests = random.randint(1, 100)
        print(f"Sending {num_requests} HTTP requests in burst")
        
        for _ in range(num_requests):
            try:
                with urllib.request.urlopen(f"http://localhost:{PORT}/") as response:
                    response.read()  # Read to complete the request
            except Exception as e:
                print(f"Error sending request: {e}")
            # Small delay between requests to avoid overwhelming
            time.sleep(random.uniform(0.01, 0.1))

# Main function to start everything
if __name__ == "__main__":
    # Start HTTP server in a daemon thread
    server_thread = threading.Thread(target=start_http_server, daemon=True)
    server_thread.start()
    
    # Start CPU spike thread
    cpu_thread = threading.Thread(target=cpu_spike_thread, daemon=True)
    cpu_thread.start()
    
    # Start HTTP spike thread
    http_thread = threading.Thread(target=http_spike_thread, daemon=True)
    http_thread.start()
    
    # Keep the main thread alive
    print("Test app running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.")