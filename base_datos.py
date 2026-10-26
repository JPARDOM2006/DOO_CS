import sqlite3

DB_NAME = "sistema_canchas.db"


def inicializar_base_datos():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        script = """
        PRAGMA foreign_keys = ON;

        -- TABLA PADRE: USUARIOS
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            documento TEXT UNIQUE,
            telefono TEXT,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            tipo_usuario TEXT NOT NULL,
            fecha_registro TEXT NOT NULL
        );

        -- TABLAS HIJAS
        CREATE TABLE IF NOT EXISTS clientes (
            id_usuario INTEGER PRIMARY KEY,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS empleados (
            id_usuario INTEGER PRIMARY KEY,
            cargo TEXT,
            salario TEXT,
            horario TEXT,
            direccion TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS administradores (
            id_usuario INTEGER PRIMARY KEY,
            cargo TEXT,
            salario TEXT,
            direccion TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
        );

        -- ESTABLECIMIENTOS
        CREATE TABLE IF NOT EXISTS establecimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_establecimiento TEXT NOT NULL,
            ubicacion TEXT NOT NULL
        );

        -- TARIFAS
        CREATE TABLE IF NOT EXISTS tarifas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor_hora REAL NOT NULL,
            dias_semana TEXT,
            valor_dia REAL DEFAULT 0,
            valor_ubicacion REAL DEFAULT 0,
            valor_tipo_jornada REAL DEFAULT 0
        );

        -- HORARIOS
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT
        );

        -- CANCHAS
        CREATE TABLE IF NOT EXISTS canchas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_establecimiento INTEGER,
            id_tarifa INTEGER,
            nombre_cancha TEXT NOT NULL,
            tipo_cancha TEXT NOT NULL,
            precio REAL NOT NULL,
            horario TEXT,
            estado TEXT DEFAULT 'Disponible',
            FOREIGN KEY (id_establecimiento) REFERENCES establecimientos(id),
            FOREIGN KEY (id_tarifa) REFERENCES tarifas(id)
        );

        -- RESERVAS
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_cancha INTEGER,
            fecha_apartada TEXT NOT NULL,
            hora_inicio TEXT NOT NULL,
            hora_final TEXT NOT NULL,
            duracion REAL NOT NULL,
            estado TEXT DEFAULT 'Pendiente',
            total_reserva REAL DEFAULT 0.0,
            abono REAL DEFAULT 0.0,
            FOREIGN KEY (id_cliente) REFERENCES usuarios(id),
            FOREIGN KEY (id_cancha) REFERENCES canchas(id)
        );

        -- METODOS DE PAGO
        CREATE TABLE IF NOT EXISTS metodos_pago (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_pago TEXT NOT NULL,
            descripcion TEXT
        );

        -- PAGOS
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_reserva INTEGER,
            id_metodo_pago INTEGER,
            fecha_pago TEXT NOT NULL,
            valor REAL NOT NULL,
            comprobante TEXT,
            estado TEXT DEFAULT 'Registrado',
            FOREIGN KEY (id_reserva) REFERENCES reservas(id),
            FOREIGN KEY (id_metodo_pago) REFERENCES metodos_pago(id)
        );
        """

        cursor.executescript(script)
        conn.commit()
        print("[DB] Base de datos inicializada correctamente (sistema_canchas.db)")
    except sqlite3.Error as e:
        print(f"[DB ERROR] Error al inicializar la base de datos: {e}")
    finally:
        if conn:
            conn.close()
