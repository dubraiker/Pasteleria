from fastapi import HTTPException, status
from app.core.database import Database
from app.models.iot import DispositivoIoTCreate, LecturaSensorCreate, AlertaEmergenciaCreate

class IoTRepository:
    def __init__(self):
        self.db = Database()

    
    def registrar_dispositivo(self, dispositivo: DispositivoIoTCreate):
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        
        cursor = conn.cursor()
        query = """
            INSERT INTO dispositivo_iot (nombre, codigo_mac, ubicacion)
            VALUES (%s, %s, %s) RETURNING id;
        """
        try:
            cursor.execute(query, (dispositivo.nombre, dispositivo.codigo_mac, dispositivo.ubicacion))
            nuevo_id = cursor.fetchone()['id']
            conn.commit()
            return nuevo_id
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al registrar dispositivo: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def listar_dispositivos(self):
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM dispositivo_iot WHERE estado = TRUE ORDER BY id ASC;")
            dispositivos = cursor.fetchall()
            return dispositivos
        finally:
            cursor.close()
            conn.close()

    # --- TELEMETRÍA (LECTURA DE SENSORES) ---
    def registrar_lectura(self, lectura: LecturaSensorCreate):
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        
        cursor = conn.cursor()
        query = """
            INSERT INTO lectura_sensor (id_dispositivo, temperatura, humedad, movimiento_detectado)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """
        try:
            cursor.execute(query, (
                lectura.id_dispositivo,
                lectura.temperatura,
                lectura.humedad,
                lectura.movimiento_detectado
            ))
            nuevo_id = cursor.fetchone()['id']
            conn.commit()
            return nuevo_id
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al guardar lectura: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def obtener_ultimas_lecturas(self, id_dispositivo: int, limite: int = 10):
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        
        cursor = conn.cursor()
        query = """
            SELECT * FROM lectura_sensor 
            WHERE id_dispositivo = %s AND estado = TRUE 
            ORDER BY creado DESC LIMIT %s;
        """
        try:
            cursor.execute(query, (id_dispositivo, limite))
            lecturas = cursor.fetchall()
            return lecturas
        finally:
            cursor.close()
            conn.close()

    # --- ALERTAS DE EMERGENCIA ---
    def crear_alerta(self, alerta: AlertaEmergenciaCreate):
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        
        cursor = conn.cursor()
        query = """
            INSERT INTO alerta_emergencia (id_dispositivo, id_tipo_alerta, mensaje)
            VALUES (%s, %s, %s) RETURNING id;
        """
        try:
            cursor.execute(query, (alerta.id_dispositivo, alerta.id_tipo_alerta, alerta.mensaje))
            nuevo_id = cursor.fetchone()['id']
            conn.commit()
            return nuevo_id
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al generar alerta: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def obtener_alertas_pendientes(self):
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        
        cursor = conn.cursor()
        query = """
            SELECT a.id, a.id_dispositivo, a.id_tipo_alerta, a.id_usuario_atencion,
                   a.mensaje, a.atendida, a.fecha_atencion, a.creado,
                   t.nombre as tipo_alerta_nombre, t.nivel_riesgo, d.nombre as dispositivo_nombre
            FROM alerta_emergencia a
            LEFT JOIN tipo_alerta t ON a.id_tipo_alerta = t.id
            LEFT JOIN dispositivo_iot d ON a.id_dispositivo = d.id
            WHERE a.atendida = FALSE AND a.estado = TRUE
            ORDER BY a.creado DESC;
        """
        try:
            cursor.execute(query)
            alertas = cursor.fetchall()
            return alertas
        finally:
            cursor.close()
            conn.close()

    def atender_alerta(self, alerta_id: int, id_usuario: int):
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        
        cursor = conn.cursor()
        query = """
            UPDATE alerta_emergencia
            SET atendida = TRUE, fecha_atencion = CURRENT_TIMESTAMP, id_usuario_atencion = %s
            WHERE id = %s AND estado = TRUE RETURNING id;
        """
        try:
            cursor.execute(query, (id_usuario, alerta_id))
            actualizado = cursor.fetchone()
            conn.commit()
            return actualizado is not None
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al atender alerta: {str(e)}")
        finally:
            cursor.close()
            conn.close()