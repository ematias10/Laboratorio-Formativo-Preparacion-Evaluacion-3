-- ==============================================================================
-- INACAP - TECNOLOGÍAS DE LA INFORMACIÓN Y CIBERSEGURIDAD
-- Asignatura: Programación Orientada a Objeto Seguro (TI3021)
-- Script DDL: Estructura de Base de Datos para Unidad 3 (schema_u3.sql)
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS ecotech_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ecotech_db;

-- 1. Tabla de Usuarios para Autenticación Segura (Clase 21 / ES3)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL, -- Espacio suficiente para salt_hex$hash_hex de PBKDF2
    rol VARCHAR(20) NOT NULL DEFAULT 'ADMIN',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Tabla de Indicadores Económicos para Consumo de APIs (Clase 22 y 23 / ES3)
CREATE TABLE IF NOT EXISTS indicadores_economicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    valor DECIMAL(12, 2) NOT NULL,       -- Precisión monetaria para UF, Dólar, etc.
    unidad_medida VARCHAR(30) NOT NULL,
    fecha_indicador DATE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Clave única compuesta: impide registros duplicados del mismo indicador en la misma fecha
    UNIQUE KEY uq_indicador_fecha (codigo, fecha_indicador)
) ENGINE=InnoDB;
