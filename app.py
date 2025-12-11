#!/usr/bin/env python3
"""
Servidor HTTP simple que responde Hola Mundo
"""
import http.server
import socketserver
import sys
import os
import json
from datetime import datetime
import random

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

PORT = 3000

# Configuración de base de datos desde variables de entorno
DB_HOST = os.environ.get('DATABASE_HOST', 'mi-postgres-postgresql-primary.susanarodas-dev.svc.cluster.local')
DB_PORT = os.environ.get('DATABASE_PORT', '5432')
DB_NAME = os.environ.get('DATABASE_NAME', 'postgres')
DB_USER = os.environ.get('DATABASE_USER', 'postgres')
DB_PASSWORD = os.environ.get('DATABASE_PASSWORD', '')

# Lista de nombres aleatorios
NOMBRES = [
    "Juan García", "María López", "Carlos Rodríguez", "Ana Martínez", "Miguel Sánchez",
    "Laura Pérez", "Antonio Fernández", "Isabel Gómez", "José Torres", "Carmen Díaz",
    "Francisco Ruiz", "Dolores Moreno", "Vicente Castro", "Rosa Romero", "Manuel Herrera"
]

def init_database():
    """Inicializa la base de datos con la tabla users"""
    if not POSTGRES_AVAILABLE:
        print("Advertencia: psycopg2 no está instalado", file=sys.stderr)
        return
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Verificar si la tabla existe y tiene registros
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            record_count = cursor.fetchone()[0]
            if record_count > 0:
                print("La tabla 'users' ya existe y contiene registros. No se realizarán cambios.", file=sys.stdout)
                cursor.close()
                conn.close()
                return
        except psycopg2.Error:
            # La tabla no existe, procederemos a crearla
            pass
        
        # Crear tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        """)
        
        # Verificar nuevamente si hay registros (por si acaso)
        cursor.execute("SELECT COUNT(*) FROM users")
        record_count = cursor.fetchone()[0]
        
        if record_count == 0:
            # Insertar 5 registros con nombres aleatorios
            nombres_seleccionados = random.sample(NOMBRES, 5)
            for nombre in nombres_seleccionados:
                cursor.execute("INSERT INTO users (name) VALUES (%s)", (nombre,))
            print(f"Tabla 'users' inicializada con 5 registros", file=sys.stdout)
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}", file=sys.stderr)
        sys.stderr.flush()

def get_users():
    """Conecta a PostgreSQL y obtiene los usuarios"""
    if not POSTGRES_AVAILABLE:
        return {"error": "psycopg2 no está instalado"}
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id, name FROM users")
            rows = cursor.fetchall()
            users = [{"id": row[0], "name": row[1]} for row in rows]
            cursor.close()
            conn.close()
            return {"users": users}
        except psycopg2.Error as e:
            # Si la tabla no existe, intentar crearla
            if "relation" in str(e) and "does not exist" in str(e):
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL
                    )
                """)
                # Insertar 5 registros con nombres aleatorios
                nombres_seleccionados = random.sample(NOMBRES, 5)
                for nombre in nombres_seleccionados:
                    cursor.execute("INSERT INTO users (name) VALUES (%s)", (nombre,))
                conn.commit()
                
                # Obtener los usuarios recién creados
                cursor.execute("SELECT id, name FROM users")
                rows = cursor.fetchall()
                users = [{"id": row[0], "name": row[1]} for row in rows]
                cursor.close()
                conn.close()
                return {"users": users}
            else:
                return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

class HolaMundoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Solicitud GET recibida PEPITO", file=sys.stdout)
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
        elif self.path == '/users':
            print(f"[{timestamp}] se llamo al endpoints /users", file=sys.stdout)
            sys.stdout.flush()
            result = get_users()
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
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
    # Inicializar la base de datos
    init_database()
    
    with socketserver.TCPServer(("", PORT), HolaMundoHandler) as httpd:
        print(f"Servidor corriendo en puerto {PORT}")
        print("Presiona Ctrl+C para detener")
        httpd.serve_forever()
