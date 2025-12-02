#!/usr/bin/env python3
"""
Servidor HTTP simple que responde Hola Mundo
"""
import http.server
import socketserver

PORT = 3000

class HolaMundoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'<h1>Hola Mundo OpenShift</h1>')
    
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format%args}")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), HolaMundoHandler) as httpd:
        print(f"Servidor corriendo en puerto {PORT}")
        print("Presiona Ctrl+C para detener")
        httpd.serve_forever()