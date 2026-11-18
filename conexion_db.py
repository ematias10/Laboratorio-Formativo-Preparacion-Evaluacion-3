# ==============================================================================
# INACAP - TECNOLOGÍAS DE LA INFORMACIÓN Y CIBERSEGURIDAD
# Asignatura: Programación Orientada a Objeto Seguro (TI3021)
# Módulo: Conexión Segura a Base de Datos MySQL (conexion_db.py)
# ==============================================================================
"""
Este módulo proporciona la clase ConexionDB, encargada de administrar el ciclo
de vida de las conexiones hacia el motor MySQL de forma centralizada y segura.

"""

import pymysql
from pymysql.cursors import DictCursor
from typing import Optional


class ConexionDB:
    """
    Gestor centralizado de conexiones hacia la base de datos ecotech_db.
    """
    def __init__(self, host: str = "localhost", user: str = "root", password: str = "", database: str = "ecotech_db", port: int = 3306):
        # Atributos privados: protegen la configuración interna del objeto
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__port = port
        self.__conexion: Optional[pymysql.Connection] = None

    def conectar(self) -> Optional[pymysql.Connection]:
        """
        Establece y retorna una conexión activa hacia la base de datos MySQL.
        Si la conexión falla, captura el error de forma segura y retorna None.
        """
        try:
            self.__conexion = pymysql.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.__database,
                port=self.__port,
                cursorclass=DictCursor,     # Retorna registros como diccionarios {'columna': valor}
                autocommit=False,           # Transacciones manuales para control estricto de commit/rollback
                charset="utf8mb4"           # Soporte completo para caracteres en español y símbolos
            )
            return self.__conexion
        except pymysql.MySQLError as err:
            # En producción, este error se registra en un log interno protegido
            print(f"❌ [Seguridad] Error al conectar con la base de datos: {err}")
            return None

    def cerrar(self):
        """
        Cierra la conexión activa de forma segura liberando los recursos del servidor.
        """
        if self.__conexion and self.__conexion.open:
            self.__conexion.close()
            # print("🔒 Conexión con base de datos cerrada de forma limpia.")
