#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class HTTPSDHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"📥 Request: {self.path} from {self.client_address}")
        if self.path == '/targets':
            # Targets válidos en formato HTTP SD
            targets = [
                {
                    "targets": ["localhost:9090"],
                    "labels": {
                        "__meta_creator": "alfred",
                    }
                }
            ]
            
            self.send_response(200)     # required response for HTTP SD config
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(targets, indent=2).encode())
            print(f"✅ Served {len(targets)} target groups")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8083), HTTPSDHandler)
    print("🚀 HTTP SD server running on http://localhost:8080/targets")
    print("📋 Test with: curl http://localhost:8080/targets")
    server.serve_forever()