# ==============================================================================
# INACAP - TECNOLOGÍAS DE LA INFORMACIÓN Y CIBERSEGURIDAD
# Asignatura: Programación Orientada a Objeto Seguro (TI3021)
# Módulo: Autenticación y Hashing Criptográfico (hash_seguro.py)
# ==============================================================================
"""
MÓDULO DE AUTENTICACIÓN Y SEGURIDAD
Implementa el hashing de contraseñas con PBKDF2 y Salt, junto con el DAO de usuarios.
"""

import os
import hashlib
import hmac
import pymysql
from conexion_db import ConexionDB


class GestorSeguridad:
    """
    Utilidades para generación y validación de contraseñas con PBKDF2 y Salt.
    """
    ITERACIONES = 100000
    ALGORITMO = "sha256"

    @staticmethod
    def generar_hash(password_plano):
        """
        Genera un hash con Salt aleatorio y retorna formato '<salt_hex>$<hash_hex>'.
        """
        # Sal aleatoria de 16 bytes
        salt_bytes = os.urandom(16)

        # Derivación con PBKDF2
        hash_bytes = hashlib.pbkdf2_hmac(
            GestorSeguridad.ALGORITMO,
            password_plano.encode("utf-8"),
            salt_bytes,
            GestorSeguridad.ITERACIONES
        )

        return f"{salt_bytes.hex()}${hash_bytes.hex()}"

    @staticmethod
    def verificar_password(password_plano, hash_almacenado):
        """
        Compara la contraseña en texto plano contra el hash guardado.
        """
        try:
            if not hash_almacenado or "$" not in hash_almacenado:
                return False

            salt_hex, hash_esperado = hash_almacenado.split("$", 1)
            salt_bytes = bytes.fromhex(salt_hex)

            hash_calculado = hashlib.pbkdf2_hmac(
                GestorSeguridad.ALGORITMO,
                password_plano.encode("utf-8"),
                salt_bytes,
                GestorSeguridad.ITERACIONES
            ).hex()

            # Comparación en tiempo constante para evitar Timing Attacks
            return hmac.compare_digest(hash_calculado, hash_esperado)
        except Exception:
            return False


class UsuarioDAO:
    """
    Acceso a datos para usuarios en MySQL.
    """
    def __init__(self, gestor_conexion):
        self.gestor = gestor_conexion

    def registrar_usuario(self, username, password_plano, rol="ADMIN"):
        """
        Registra un usuario guardando únicamente el hash generado.
        """
        hash_seguro = GestorSeguridad.generar_hash(password_plano)
        sql = """
            INSERT INTO usuarios (username, password_hash, rol)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE password_hash = VALUES(password_hash), rol = VALUES(rol);
        """
        conexion = self.gestor.conectar()
        if not conexion:
            return False

        try:
            with conexion.cursor() as cursor:
                cursor.execute(sql, (username.strip().lower(), hash_seguro, rol.strip().upper()))
            conexion.commit()
            return True
        except pymysql.MySQLError as err:
            conexion.rollback()
            print(f"Error al registrar usuario: {err}")
            return False
        finally:
            self.gestor.cerrar()

    def autenticar(self, username, password_plano):
        """
        Valida las credenciales contra la BD. Retorna perfil si es válido o None.
        """
        sql = "SELECT id, username, password_hash, rol, activo FROM usuarios WHERE username = %s LIMIT 1;"
        conexion = self.gestor.conectar()
        if not conexion:
            return None

        try:
            with conexion.cursor() as cursor:
                cursor.execute(sql, (username.strip().lower(),))
                usuario = cursor.fetchone()

            if not usuario:
                return None

            if not usuario.get("activo", False):
                print("Cuenta inactiva.")
                return None

            if GestorSeguridad.verificar_password(password_plano, usuario["password_hash"]):
                return {
                    "id": usuario["id"],
                    "username": usuario["username"],
                    "rol": usuario["rol"]
                }
            return None
        except pymysql.MySQLError as err:
            print(f"Error en autenticación: {err}")
            return None
        finally:
            self.gestor.cerrar()


# ==============================================================================
# EJECUCIÓN DE PRUEBA DEL MÓDULO
# ==============================================================================
if __name__ == "__main__":
    print("--- Probando Criptografía y Hashing ---")
    password_prueba = "ClaveSecreta2026!"

    # 1. Prueba de Hashing
    hash_generado = GestorSeguridad.generar_hash(password_prueba)
    print(f"1. Password original: {password_prueba}")
    print(f"   Hash con Salt:     {hash_generado}")

    # 2. Prueba de Verificación
    valida = GestorSeguridad.verificar_password(password_prueba, hash_generado)
    print(f"2. ¿Validación correcta con password real?: {valida}")

    invalida = GestorSeguridad.verificar_password("clave_erronea", hash_generado)
    print(f"   ¿Validación con password incorrecta?:   {invalida}")

    # 3. Prueba opcional con base de datos
    print("\n3. Probando UsuarioDAO con MySQL:")
    conexion = ConexionDB()
    dao = UsuarioDAO(conexion)
    if dao.registrar_usuario("admin", password_prueba):
        print("   -> Usuario 'admin' registrado/actualizado en base de datos.")
        perfil = dao.autenticar("admin", password_prueba)
        print(f"   -> Autenticación exitosa. Perfil obtenido: {perfil}")
    else:
        print("   -> (Servidor MySQL no disponible o error de conexión, verificar servicio local)")
