# ==============================================================================
# INACAP - TECNOLOGÍAS DE LA INFORMACIÓN Y CIBERSEGURIDAD
# Asignatura: Programación Orientada a Objeto Seguro (TI3021)
# Módulo: Persistencia Relacional (indicador_dao.py)
# ==============================================================================
"""
MÓDULO DE PERSISTENCIA RELACIONAL
---------------------------------
Implementa el patrón DAO para interactuar con la tabla 'indicadores_economicos'.
"""

import pymysql
from conexion_db import ConexionDB
from cliente_api import IndicadorFinanciero


class IndicadorDAO:
    """
    Capa de acceso a datos para la tabla 'indicadores_economicos'.
    """
    def __init__(self, gestor_conexion):
        self.gestor = gestor_conexion

    def guardar_o_actualizar(self, indicador):
        """
        Inserta un nuevo indicador o actualiza su valor si ya existe en la fecha.
        """
        sql = """
            INSERT INTO indicadores_economicos (codigo, nombre, valor, unidad_medida, fecha_indicador)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                valor = VALUES(valor),
                nombre = VALUES(nombre),
                unidad_medida = VALUES(unidad_medida),
                fecha_registro = CURRENT_TIMESTAMP;
        """
        parametros = (
            indicador.codigo,
            indicador.nombre,
            indicador.valor,
            indicador.unidad_medida,
            indicador.fecha
        )

        conexion = self.gestor.conectar()
        if not conexion:
            return False

        try:
            with conexion.cursor() as cursor:
                cursor.execute(sql, parametros)
            conexion.commit()
            return True
        except pymysql.MySQLError as err:
            conexion.rollback()
            print(f"Error al persistir indicador: {err}")
            return False
        finally:
            self.gestor.cerrar()

    def obtener_ultimo(self, codigo):
        """
        Recupera el último registro almacenado para un indicador según su fecha.
        Permite soportar la resiliencia en caso de caída de la API.
        """
        sql = """
            SELECT codigo, nombre, valor, unidad_medida, fecha_indicador
            FROM indicadores_economicos
            WHERE codigo = %s
            ORDER BY fecha_indicador DESC
            LIMIT 1;
        """
        conexion = self.gestor.conectar()
        if not conexion:
            return None

        try:
            with conexion.cursor() as cursor:
                cursor.execute(sql, (codigo.strip().lower(),))
                fila = cursor.fetchone()

            if not fila:
                return None

            return IndicadorFinanciero(
                fila["codigo"],
                fila["nombre"],
                float(fila["valor"]),
                str(fila["fecha_indicador"]),
                fila["unidad_medida"]
            )
        except pymysql.MySQLError as err:
            print(f"Error al obtener último indicador: {err}")
            return None
        finally:
            self.gestor.cerrar()

    def listar_todos(self):
        """
        Retorna la lista de todos los indicadores almacenados en la base de datos.
        """
        sql = "SELECT codigo, nombre, valor, unidad_medida, fecha_indicador FROM indicadores_economicos ORDER BY fecha_indicador DESC;"
        conexion = self.gestor.conectar()
        if not conexion:
            return []

        try:
            with conexion.cursor() as cursor:
                cursor.execute(sql)
                filas = cursor.fetchall()

            resultado = []
            for f in filas:
                resultado.append(
                    IndicadorFinanciero(
                        f["codigo"],
                        f["nombre"],
                        float(f["valor"]),
                        str(f["fecha_indicador"]),
                        f["unidad_medida"]
                    )
                )
            return resultado
        except pymysql.MySQLError as err:
            print(f"Error al listar: {err}")
            return []
        finally:
            self.gestor.cerrar()


# ==============================================================================
# EJECUCIÓN DE PRUEBA DEL MÓDULO
# ==============================================================================
if __name__ == "__main__":
    print("--- Probando IndicadorDAO ---")
    
    # 1. Crear una instancia de prueba en memoria
    indicador_demo = IndicadorFinanciero("uf", "Unidad de Fomento", 37950.25, "2026-11-18", "Pesos")
    print(f"1. Instancia creada: {indicador_demo}")

    # 2. Probar persistencia si MySQL está disponible
    print("\n2. Probando operaciones en MySQL:")
    conexion = ConexionDB()
    dao = IndicadorDAO(conexion)

    if dao.guardar_o_actualizar(indicador_demo):
        print("   -> Indicador guardado/actualizado con éxito.")
        ultimo = dao.obtener_ultimo("uf")
        print(f"   -> Último indicador recuperado: {ultimo}")
        todos = dao.listar_todos()
        print(f"   -> Total de registros en tabla: {len(todos)}")
    else:
        print("   -> (Servidor MySQL no disponible o error de conexión, verificar servicio local)")
