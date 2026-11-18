# ==============================================================================
# INACAP - TECNOLOGÍAS DE LA INFORMACIÓN Y CIBERSEGURIDAD
# Asignatura: Programación Orientada a Objeto Seguro (TI3021)
# Módulo: Consumo de APIs y Deserialización (cliente_api.py)
# ==============================================================================
"""
MÓDULO DE CONSUMO DE SERVICIOS EXTERNOS (APIs)
"""

import requests
import json
from datetime import datetime


class IndicadorFinanciero:
    """
    Clase que representa un indicador económico.
    Se entrega simplificada sin properties ni atributos privados.
    """
    def __init__(self, codigo, nombre, valor, fecha, unidad_medida):
        self.codigo = codigo
        self.nombre = nombre
        self.valor = valor
        self.fecha = fecha
        self.unidad_medida = unidad_medida

    def __str__(self):
        return f"[{self.codigo}] {self.nombre}: {self.valor} {self.unidad_medida} ({self.fecha})"


class ClienteAPIIndicadores:
    """
    Cliente HTTP simplificado para consumir la API pública de indicadores.
    """
    URL_BASE = "https://findic.cl/api"

    def __init__(self, timeout_segundos=5):
        self.timeout = timeout_segundos

    def consultar_indicador(self, codigo_indicador):
        """
        Consulta un indicador específico y retorna una instancia de IndicadorFinanciero.
        """
        endpoint = f"{self.URL_BASE}/{codigo_indicador}"
        try:
            respuesta = requests.get(endpoint, timeout=self.timeout)
            respuesta.raise_for_status()
            data = respuesta.json()

            serie = data.get("serie", [])
            if not serie:
                print(f"No se encontraron datos para {codigo_indicador}")
                return None

            ultimo = serie[0]
            fecha_limpia = str(ultimo.get("fecha", ""))[:10]

            return IndicadorFinanciero(
                codigo_indicador,
                data.get("nombre", "Indicador"),
                float(ultimo.get("valor", 0)),
                fecha_limpia,
                data.get("unidad_medida", "Pesos")
            )

        except Exception as err:
            print(f"Error procesando datos: {err}")
            return None

    def consultar_serie_historica(self, codigo_indicador, limite=3):
        """
        Obtiene los últimos N registros históricos de un indicador.
        """
        endpoint = f"{self.URL_BASE}/{codigo_indicador}"
        lista = []
        try:
            respuesta = requests.get(endpoint, timeout=self.timeout)
            respuesta.raise_for_status()
            data = respuesta.json()

            nombre = data.get("nombre", codigo_indicador)
            unidad = data.get("unidad_medida", "Pesos")

            for item in data.get("serie", [])[:limite]:
                fecha_limpia = str(item.get("fecha", ""))[:10]
                lista.append(
                    IndicadorFinanciero(
                        codigo_indicador,
                        nombre,
                        float(item.get("valor", 0)),
                        fecha_limpia,
                        unidad
                    )
                )
            return lista
        except Exception as err:
            print(f"Error al consultar serie: {err}")
            return []


# ==============================================================================
# EJECUCIÓN DE PRUEBA DEL MÓDULO
# ==============================================================================
if __name__ == "__main__":
    print("--- Probando Cliente API ---")
    cliente = ClienteAPIIndicadores(timeout_segundos=5)

    print("\n1. Consultando indicador 'uf' en tiempo real:")
    uf = cliente.consultar_indicador("uf")
    if uf:
        print("   Resultado:", uf)

    print("\n2. Consultando serie histórica de 'dolar' (últimos 3 registros):")
    historico = cliente.consultar_serie_historica("dolar", limite=3)
    for reg in historico:
        print("  ", reg)
