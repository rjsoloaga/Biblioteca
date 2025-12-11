import psycopg2
from tkinter import messagebox
import os


# Credenciales de la Base de Datos
DB_HOST = "localhost"
DB_NAME = "biblioteca"
DB_USER = "biblioteca"
DB_PASS = "biblioteca"
DB_PORT = "5432"


def cargar_config():
    config = {}

    try:
        if not os.path.exists('config.txt'):
            messagebox.showerror("Error", "No se encontró el archivo config.txt\nUsando valores por defecto")
            return ('HOST=localhost', 'DB=biblioteca', 'USER=biblioteca', 'PASS=biblioteca', 'PORT=5432')
        
        with open("config.txt", "r") as archivo:
            for linea in archivo:
                linea = linea .strip()
                if not linea or '=' not in linea: continue
                clave, valor = linea.split("=",1)
                config[clave] = valor
        return config
    except Exception as e:
        messagebox.showerror("Error", "No se encontró el archivo de configuración")
        print(f"Error al cargar config: {e}")
        return None

CONF = cargar_config()



# Funciones de la Base de Datos
def conexionDB():
    try:
        conexion = psycopg2.connect(
            host = CONF['HOST'],
            database = CONF['DB'],
            user = CONF['USER'],
            password = CONF['PASS'],
            port = CONF['PORT'],
            connect_timeout = 3
        )
        return conexion
    except Exception as e:
        print(f"Error grave de conexion: {e}")
        messagebox.showerror("Error", "No se pudo conectar a la Base de Datos (Docker)")
        return None


def crear_tabla():
    conn = conexionDB()
    if conn is None: return

    with conn.cursor() as cursor:
        # 1. Tabla Tipo Recurso
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tipo_recurso (
                id_tipo_recurso SERIAL PRIMARY KEY,
                descripcion VARCHAR(50) NOT NULL,
                sale_de_institucion BOOLEAN DEFAULT FALSE
            );
        """)
        
        # 2. Cargar datos iniciales
        cursor.execute("SELECT COUNT(*) FROM tipo_recurso;") 
        cantidad = cursor.fetchone()[0]
        if cantidad == 0:
            print("Inicializando Tipos de Recursos...")
            cursor.execute("""
            INSERT INTO tipo_recurso (descripcion, sale_de_institucion) VALUES
            ('Libro', TRUE),
            ('Proyector', FALSE),
            ('Netbook', FALSE);
            """)

        # 3. Tabla Inventario (Con correcciones de FK y Campos)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventario(
            id_inventario SERIAL PRIMARY KEY,
            tipo_recurso_id INT NOT NULL DEFAULT 1,
            titulo VARCHAR(255) NOT NULL,
            autor VARCHAR(255) NOT NULL,
            signatura VARCHAR(50) NOT NULL,
            estado VARCHAR(50) DEFAULT 'Disponible',
            restriccion_domicilio BOOLEAN DEFAULT FALSE,
            numero_inventario VARCHAR(50) NOT NULL UNIQUE,
            FOREIGN KEY (tipo_recurso_id) REFERENCES tipo_recurso(id_tipo_recurso)
            );
        """)
        conn.commit()
    conn.close()
    print("Base de datos verificada.")


def guardar_inventario(tipo_recurso_id, titulo, autor, numero_inventario, signatura):
    conn = conexionDB()
    if conn is None: return False

    try:
        with conn.cursor() as cursor:
            # Orden de variables CORREGIDO
            sql = """
            INSERT INTO inventario
            (tipo_recurso_id, titulo, autor, numero_inventario, signatura, estado)
            VALUES (%s, %s, %s, %s, %s, 'Disponible')
            """
            cursor.execute(sql, (tipo_recurso_id, titulo, autor, numero_inventario, signatura))
            
            conn.commit()
            conn.close()
            return True
            
    except psycopg2.errors.UniqueViolation:
            messagebox.showerror("Error", "¡Duplicado! El número de inventario YA existe.")
            conn.close()
            return False
    except Exception as e:
            messagebox.showerror("Error", f"Error SQL: {e}")
            print(f"Detalle error: {e}")
            conn.close()
            return False


def actualizar_inventario(id_inventario, titulo, autor, signatura, numero_inventario):
    conn = conexionDB()
    if conn is None: return False

    try:
        with conn.cursor() as cursor:
            sql = """
            UPDATE inventario
            SET titulo = %s, autor = %s, signatura = %s, numero_inventario = %s
            WHERE id_inventario = %s
            """
            cursor.execute(sql, (titulo, autor, signatura, numero_inventario, id_inventario))
            conn.commit()
            conn.close()
            return True
    except psycopg2.errors.UniqueViolation:
        messagebox.showerror("Error", "Ese número de inventario ya existe en otro libro")
        conn.close()
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Error al Actualizar: {e}")
        conn.close()
        return False


def eliminar_inventario(id_inventario):
    conn = conexionDB()
    if conn is None: return False

    try:
        with conn.cursor() as cursor:
            sql = """ DELETE FROM inventario WHERE id_inventario = %s """
            cursor.execute(sql, (id_inventario,))
            conn.commit()
            conn.close()
            return True
    except Exception as e:
            messagebox.showerror("Error", f"Error SQL: {e}")
            print(f"Detalle error: {e}")
            conn.close()
            return False
    


def listar_inventario():
    conn = conexionDB()
    if conn is None: return []

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_inventario, titulo, autor, signatura, numero_inventario FROM inventario ORDER BY id_inventario DESC")
            registros = cursor.fetchall()
            conn.close()
            return registros
    except Exception as e:
        messagebox.showerror("Error", f"Error SQL: {e}")
        print(f"Detalle error: {e}")
        conn.close()
        return []


def listar_autores():
    conn = conexionDB()
    if conn is None: return []

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT autor FROM inventario ORDER BY autor ASC")
            registros = cursor.fetchall()
            conn.close()
            return [r[0] for r in registros]
    except Exception as e:
        messagebox.showerror("Error", f"Error SQL: {e}")
        print(f"Detalle error: {e}")
        conn.close()
        return []


def listar_signaturas():
    conn = conexionDB()
    if conn is None: return []

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT signatura FROM inventario ORDER BY signatura ASC")
            registros = cursor.fetchall()
            conn.close()
            return [r[0] for r in registros]
    except Exception as e:
        messagebox.showerror("Error", f"Error SQL: {e}")
        print(f"Detalle error: {e}")
        conn.close()
        return []