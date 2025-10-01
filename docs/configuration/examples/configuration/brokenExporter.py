#!/usr/bin/env python3
"""
Simulador de exporter problemático que demuestra fallback de protocolos
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

class BrokenExporterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            accept_header = self.headers.get('Accept', '')
            print(f"📥 Request Accept: {accept_header}")
            
            # Simular diferentes tipos de problemas
            problem = random.choice(['blank', 'unparsable', 'invalid_content_type', 'valid'])
            
            if problem == 'blank':
                # Respuesta en blanco
                print("❌ Returning BLANK response")
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'')  # Respuesta vacía
                
            elif problem == 'unparsable':
                # Contenido no parseable
                print("❌ Returning UNPARSABLE content")
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain;version=0.0.4')
                self.end_headers()
                self.wfile.write(b'This is not valid metrics format!\nRandom garbage data...')
                
            elif problem == 'invalid_content_type':
                # Content-Type inválido
                print("❌ Returning INVALID Content-Type")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')  # Tipo incorrecto
                self.end_headers()
                # Contenido válido pero Content-Type incorrecto
                metrics = """# HELP test_metric A test metric
# TYPE test_metric counter
test_metric{label="value"} 123
"""
                self.wfile.write(metrics.encode())
                
            else:
                # Respuesta válida (fallback exitoso)
                print("✅ Returning VALID response (fallback protocol)")
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain;version=0.0.4')  # Fallback a formato clásico
                self.end_headers()
                metrics = """# HELP test_metric A test metric
# TYPE test_metric counter
test_metric{label="broken_exporter"} 456
"""
                self.wfile.write(metrics.encode())

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 9999), BrokenExporterHandler)
    print("🔧 Broken exporter running on port 9999")
    print("🎲 Randomly returns: blank, unparsable, invalid Content-Type, or valid responses")
    server.serve_forever()