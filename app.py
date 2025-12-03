#!/usr/bin/env python3
"""
Servidor HTTP simple que responde Hola Mundo
"""
import http.server
import socketserver
import sys
from datetime import datetime

PORT = 3000

class HolaMundoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Solicitud GET recibida", file=sys.stdout)
        print(f"[{timestamp}] Path: {self.path}", file=sys.stdout)
        
        if self.path == '/startup':
            print(f"[{timestamp}] se llamo al endpoints /startup", file=sys.stdout)
            sys.stdout.flush()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'OK')
        elif self.path == '/liveness':
            print(f"[{timestamp}] se llamo al endpoints /liveness", file=sys.stdout)
            sys.stdout.flush()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'OK')
        elif self.path == '/readiness':
            print(f"[{timestamp}] se llamo al endpoints /readiness", file=sys.stdout)
            sys.stdout.flush()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            print(f"[{timestamp}] se llamo al endpoints raiz", file=sys.stdout)
            sys.stdout.flush()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<h1>Hola Mundo</h1>')
    
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.address_string()} - {format%args}", file=sys.stdout)
        sys.stdout.flush()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), HolaMundoHandler) as httpd:
        print(f"Servidor corriendo en puerto {PORT}")
        print("Presiona Ctrl+C para detener")
        httpd.serve_forever()