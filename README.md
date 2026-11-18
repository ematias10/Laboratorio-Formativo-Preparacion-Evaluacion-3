## Asignatura: Programación Orientada a Objeto Seguro (TI3021) - INACAP

---

### 📌 Descripción del Proyecto
Esta plantilla base sirve como punto de partida para la **Evaluación Sumativa 3 (ES3 - Ponderación 25%)**.
El objetivo es extender el sistema de **EcoTech Solutions**, integrando el consumo seguro de servicios web (APIs RESTful), la persistencia relacional en MySQL y la autenticación criptográfica de usuarios bajo el estándar OWASP.

---

### 📂 Estructura de la Plantilla
```text
plantilla_evaluacion_u3/
│
├── schema_u3.sql           # Script SQL para crear la base de datos y tablas requeridas en MySQL.
├── conexion_db.py          # [INTACTO] Gestor centralizado de conexiones MySQL (PyMySQL + DictCursor).
├── cliente_api.py          # [SIMPLIFICADO] Cliente HTTP funcional básico y modelo IndicadorFinanciero.
├── hash_seguro.py          # [SIMPLIFICADO] Hashing con PBKDF2, Salt y DAO de usuarios.
├── indicador_dao.py        # [SIMPLIFICADO] Persistencia relacional básica en MySQL.
└── README.md               # Este archivo con instrucciones técnicas y guía de evaluación.
```

> **NOTA IMPORTANTE:**
> 1. Cada archivo incluye al final un bloque `if __name__ == "__main__":` que puedes ejecutar de forma independiente (`python cliente_api.py`, `python hash_seguro.py`, `python indicador_dao.py`) para comprobar su funcionamiento básico.
> 2. El orquestador principal (`main.py`) **NO está incluido**. Es parte fundamental de tu evaluación diseñar e implementar dicho archivo desde cero, integrando las clases y métodos desarrollados.

---

### ⚙️ Requisitos Previos y Configuración
1. **Librerías de Python requeridas:**
   ```bash
   pip install requests pymysql
   ```
2. **Base de Datos MySQL:**
   - Inicia tu servidor MySQL local (XAMPP, WAMP o servicio Windows).
   - Ejecuta el script `schema_u3.sql` en MySQL Workbench, phpMyAdmin o terminal.
   - Revisa `conexion_db.py` en caso de requerir cambiar el usuario o contraseña de tu motor MySQL.

---

### 🎯 Tareas y Mejoras por Implementar para la Evaluación

Aunque los módulos contienen código funcional simplificado, **para obtener la máxima calificación en la evaluación debes refinar y aplicar los criterios de evaluación exigidos**:

#### 1. Consumo de Servicios Externos (`cliente_api.py`) - *Criterio 3.1.1 y 3.1.3*
- [ ] Aplicar **encapsulamiento y POO defensiva** en `IndicadorFinanciero`: atributos privados (`__`) y métodos de acceso `@property`.
- [ ] Incorporar cabeceras HTTP (`User-Agent`) en las peticiones.
- [ ] Implementar control de timeouts defensivos mediante tupla `(conexión, lectura)`.
- [ ] Manejar excepciones específicas de la librería `requests`:
  - `requests.exceptions.Timeout`
  - `requests.exceptions.ConnectionError`
  - `requests.exceptions.HTTPError`
  - `json.JSONDecodeError`
- [ ] Asegurar que el sistema no interrumpa su ejecución ante caídas del servicio web externo.

#### 2. Autenticación Criptográfica y Seguridad (`hash_seguro.py`) - *Criterio 3.1.2*
- [ ] Validar entradas del usuario para evitar valores vacíos o contraseñas débiles.
- [ ] Mantener el estándar de 100.000 iteraciones con SHA-256 y Salt aleatorio de 16 bytes.
- [ ] Asegurar la comparación en tiempo constante con `hmac.compare_digest` para evitar ataques de temporización (Timing Attacks).
- [ ] Validar estados de cuentas inactivas en la base de datos antes de permitir el acceso.

#### 3. Persistencia Relacional y Consultas Seguras (`indicador_dao.py`) - *Criterio 3.1.2 y 3.1.3*
- [ ] Erradicar cualquier riesgo de inyección SQL mediante consultas estrictamente parametrizadas (`%s`).
- [ ] Manejo transaccional estricto con `commit()` y `rollback()` ante errores de integridad.
- [ ] Implementar la consulta del último registro local (`obtener_ultimo`) para dar soporte al modo de contingencia/resiliencia.

#### 4. Orquestador y Menú Interactivo (`main.py`) - *Debe ser creado por el estudiante*
Debes crear un archivo `main.py` que contemple:
1. **Control de Acceso:**
   - Flujo de inicio de sesión obligatorio antes de desplegar el menú.
   - Límite de intentos fallidos (máximo 3) antes del bloqueo.
2. **Menú de Operaciones por Consola:**
   - Sincronizar indicadores en vivo desde la API externa y guardarlos en MySQL.
   - Listar indicadores almacenados en la base de datos local.
   - **Prueba de Resiliencia / Tolerancia a Fallos:** Demostrar que ante una falla, el sistema no se cae y recurre a la base de datos local en modo contingencia.
   - Registrar nuevos usuarios administradores con contraseñas hasheadas.
   - Opción para cerrar sesión limpiamente.

---

### 🤖 Uso de Inteligencia Artificial (Criterio 3.1.4)
Se permite y fomenta el uso de herramientas de IA generativa como apoyo al desarrollo, **siempre y cuando:**
- Analices críticamente el código sugerido por la IA para detectar vulnerabilidades.
- Estés preparado para **justificar técnicamente** cada línea de código y las decisiones de diseño adoptadas.

---

