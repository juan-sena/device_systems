# device_systems

API REST desarrollada con **FastAPI** para la gestión de usuarios, dispositivos tecnológicos y préstamos. El proyecto implementa autenticación mediante JWT, autorización por roles, operaciones CRUD, filtros avanzados, middleware personalizado y documentación automática con Swagger.

---

# Descripción

**device_systems** es una API REST diseñada para administrar el préstamo de dispositivos tecnológicos dentro de una organización.

Permite:

* Gestionar usuarios.
* Gestionar dispositivos.
* Registrar préstamos.
* Registrar devoluciones.
* Consultar el historial de préstamos.
* Filtrar información mediante parámetros de consulta.
* Proteger recursos mediante autenticación JWT y autorización por roles.

Además, incorpora buenas prácticas de desarrollo como:

* Arquitectura por capas.
* SQLAlchemy ORM.
* Migraciones con Alembic.
* Validación de datos con Pydantic v2.
* Middleware personalizado.
* Rate Limiting.
* Documentación automática mediante OpenAPI.

---

# Tecnologías utilizadas

* Python 3.x
* FastAPI
* Uvicorn
* SQLAlchemy
* Alembic
* SQLite
* Pydantic v2
* Python-JOSE (JWT)
* Passlib (bcrypt)
* SlowAPI (Rate Limiting)
* Swagger UI / OpenAPI

---

# Instalación

## Clonar el repositorio

```bash
git clone https://github.com/juan-sena/device_systems.git

cd device_systems
```

## Instalar las dependencias

```bash
pip install -r requirements.txt
```

---

# Migraciones con Alembic

## Inicializar Alembic (solo la primera vez)

```bash
alembic init alembic
```

## Crear una nueva migración

```bash
alembic revision --autogenerate -m "descripcion del cambio"
```

## Aplicar todas las migraciones

```bash
alembic upgrade head
```

## Consultar el historial

```bash
alembic history
```

---

# Ejecutar el proyecto

## Iniciar el servidor

```bash
python -m uvicorn app.main:app --reload
```

Servidor:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Redoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Autenticación

La API utiliza autenticación mediante **JWT (JSON Web Token)**.

## Registrar un usuario

```http
POST /auth/register
```

## Iniciar sesión

```http
POST /auth/login
```

El login devuelve un token con el siguiente formato:

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

## Acceder a los endpoints protegidos

1. Abrir Swagger.
2. Pulsar **Authorize**.
3. Copiar el `access_token`.
4. Pegar el token.
5. Pulsar **Authorize**.

Una vez autenticado se podrán consumir todos los endpoints protegidos.

---

# Endpoints

## Auth

| Método | Endpoint       | Descripción                                 |
| ------ | -------------- | ------------------------------------------- |
| POST   | /auth/register | Registrar usuario                           |
| POST   | /auth/login    | Iniciar sesión                              |
| GET    | /auth/me       | Obtener información del usuario autenticado |

---

## Users

| Método | Endpoint               | Descripción                     |
| ------ | ---------------------- | ------------------------------- |
| GET    | /users                 | Listar usuarios                 |
| GET    | /users/{user_id}       | Obtener usuario por ID          |
| POST   | /users                 | Crear usuario                   |
| PUT    | /users/{user_id}       | Actualizar usuario              |
| PATCH  | /users/{user_id}       | Actualizar parcialmente         |
| DELETE | /users/{user_id}       | Eliminar usuario                |
| GET    | /users/{user_id}/loans | Consultar préstamos del usuario |

---

## Devices

| Método | Endpoint                   | Descripción               |
| ------ | -------------------------- | ------------------------- |
| GET    | /devices                   | Listar dispositivos       |
| GET    | /devices/{device_id}       | Obtener dispositivo       |
| POST   | /devices                   | Crear dispositivo         |
| PUT    | /devices/{device_id}       | Actualizar dispositivo    |
| PATCH  | /devices/{device_id}       | Actualizar parcialmente   |
| DELETE | /devices/{device_id}       | Eliminar dispositivo      |
| GET    | /devices/{device_id}/loans | Historial del dispositivo |

---

## Loans

| Método | Endpoint                | Descripción                   |
| ------ | ----------------------- | ----------------------------- |
| GET    | /loans                  | Listar préstamos              |
| GET    | /loans/details          | Listar préstamos con detalles |
| GET    | /loans/{loan_id}        | Obtener préstamo              |
| POST   | /loans                  | Crear préstamo                |
| PATCH  | /loans/{loan_id}/return | Registrar devolución          |

---

# Filtros disponibles

## Dispositivos

* `GET /devices?device_type=laptop`
* `GET /devices?is_available=true`
* `GET /devices?brand=lenovo`
* `GET /devices?search=thinkpad`

## Préstamos

* `GET /loans?status=active`
* `GET /loans?user_email=ana@sena.edu.co`
* `GET /loans?device_type=laptop`


# Ejemplos de peticiones y respuestas

## Registrar usuario

**POST /auth/register**

Petición:

```json
{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "password": "Juan12345",
  "role": "admin"
}
```

Respuesta:

```json
{
  "id": 1,
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "role": "admin",
  "is_active": true
}
```

---

## Iniciar sesión

**POST /auth/login**

La autenticación utiliza el formato **OAuth2 Password Flow**.

En Swagger se deben enviar los siguientes campos:

| Campo    | Valor                                       |
| -------- | ------------------------------------------- |
| username | [juan@example.com](mailto:juan@example.com) |
| password | Juan12345                                   |

Respuesta:

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

---

## Obtener usuario autenticado

**GET /auth/me**

Respuesta:

```json
{
  "id": 1,
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "role": "admin",
  "is_active": true
}
```

---

## Crear usuario

**POST /users**

Petición:

```json
{
  "name": "Ana Pérez",
  "email": "ana@sena.edu.co",
  "password": "Ana12345",
  "role": "user",
  "is_active": true
}
```

Respuesta:

```json
{
  "id": 2,
  "name": "Ana Pérez",
  "email": "ana@sena.edu.co",
  "role": "user",
  "is_active": true,
  "created_at": "2026-06-27T22:00:00"
}
```

---

## Crear dispositivo

**POST /devices**

Petición:

```json
{
  "name": "Laptop Lenovo ThinkPad",
  "serial_number": "LEN-001",
  "device_type": "laptop",
  "brand": "Lenovo"
}
```

Respuesta:

```json
{
  "id": 1,
  "name": "Laptop Lenovo ThinkPad",
  "serial_number": "LEN-001",
  "device_type": "laptop",
  "brand": "Lenovo",
  "is_available": true,
  "created_at": "2026-06-27T22:50:56"
}
```

---

## Crear préstamo

**POST /loans**

Petición:

```json
{
  "user_id": 1,
  "device_id": 1
}
```

Respuesta:

```json
{
  "id": 1,
  "loan_date": "2026-06-27T22:51:43",
  "return_date": null,
  "status": "active",
  "user": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com"
  },
  "device": {
    "id": 1,
    "name": "Laptop Lenovo ThinkPad",
    "serial_number": "LEN-001",
    "device_type": "laptop"
  }
}
```

---

## Devolver dispositivo

**PATCH /loans/{loan_id}/return**

Respuesta:

```json
{
  "id": 1,
  "loan_date": "2026-06-27T22:51:43",
  "return_date": "2026-06-27T23:05:00",
  "status": "returned",
  "user": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com"
  },
  "device": {
    "id": 1,
    "name": "Laptop Lenovo ThinkPad",
    "serial_number": "LEN-001",
    "device_type": "laptop"
  }
}
```

---

## Consultar préstamos con filtros

**GET /loans?status=active**

Respuesta:

```json
[
  {
    "id": 1,
    "loan_date": "2026-06-27T22:51:43",
    "return_date": null,
    "status": "active",
    "user": {
      "id": 1,
      "name": "Juan Pérez",
      "email": "juan@example.com"
    },
    "device": {
      "id": 1,
      "name": "Laptop Lenovo ThinkPad",
      "serial_number": "LEN-001",
      "device_type": "laptop"
    }
  }
]

# Códigos de estado HTTP

| Código                   | Descripción                                                       |
| ------------------------ | ----------------------------------------------------------------- |
| 200 OK                   | Operación realizada correctamente.                                |
| 201 Created              | Recurso creado exitosamente.                                      |
| 204 No Content           | Recurso eliminado correctamente.                                  |
| 400 Bad Request          | Solicitud inválida o recurso duplicado.                           |
| 401 Unauthorized         | Usuario no autenticado o token inválido.                          |
| 403 Forbidden            | El usuario autenticado no tiene permisos para acceder al recurso. |
| 404 Not Found            | Recurso no encontrado.                                            |
| 409 Conflict             | Regla de negocio incumplida.                                      |
| 422 Unprocessable Entity | Error de validación de datos enviados.                            |
| 429 Too Many Requests    | Límite de solicitudes excedido (Rate Limiting).                   |

---

# Manejo de errores

## Recurso no encontrado

```json
{
    "detail": "Usuario no encontrado"
}
```

```json
{
    "detail": "Dispositivo no encontrado"
}
```

```json
{
    "detail": "Préstamo no encontrado"
}
```

Código HTTP:

```text
404 Not Found
```

---

## Datos duplicados

```json
{
    "detail": "El correo ya existe"
}
```

```json
{
    "detail": "El número de serie ya existe"
}
```

Código HTTP:

```text
400 Bad Request
```

---

## Error de autenticación

```json
{
    "detail": "Correo o contraseña incorrectos."
}
```

Código HTTP:

```text
401 Unauthorized
```

---

## Error de autorización

```json
{
    "detail": "No tienes permisos."
}
```

Código HTTP:

```text
403 Forbidden
```

---

## Regla de negocio

```json
{
    "detail": "El dispositivo no está disponible para préstamo"
}
```

```json
{
    "detail": "El préstamo ya fue devuelto"
}
```

Código HTTP:

```text
409 Conflict
```

---

## Error de validación

Código HTTP:

```text
422 Unprocessable Entity
```

---

## Límite de solicitudes

Cuando un usuario supera el número permitido de peticiones al endpoint protegido, la API responde con:

Código HTTP:

```text
429 Too Many Requests
```

---

# Funcionalidades implementadas

## Gestión de usuarios

* Registro de usuarios.
* Inicio de sesión mediante JWT.
* Consulta de usuarios.
* Actualización completa y parcial.
* Eliminación de usuarios.
* Protección mediante autenticación.

---

## Gestión de dispositivos

* Registro de dispositivos.
* Consulta de dispositivos.
* Actualización completa y parcial.
* Eliminación.
* Filtros por:

  * Tipo.
  * Marca.
  * Disponibilidad.
  * Búsqueda general.

---

## Gestión de préstamos

* Crear préstamos.
* Registrar devoluciones.
* Historial de préstamos.
* Historial por usuario.
* Historial por dispositivo.
* Filtros por estado.
* Filtros por correo.
* Filtros por tipo de dispositivo.

---

## Seguridad

* JWT Authentication.
* OAuth2 Password Flow.
* Hash de contraseñas con bcrypt.
* Protección de endpoints.
* Autorización por roles:

  * Admin.
  * Support.
  * User.

---

## Calidad del proyecto

* Middleware personalizado.
* Logging de peticiones.
* Rate Limiting con SlowAPI.
* CORS.
* Validaciones mediante Pydantic.
* Documentación automática con Swagger.
* Arquitectura organizada por capas.

---

# Estructura del proyecto

```text
device_systems/
│
├── app/
│   ├── auth/
│   │   ├── auth_routes.py
│   │   ├── auth_service.py
│   │   └── security.py
│   │
│   ├── config/
│   │   └── limiter.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── dependencies/
│   │   ├── auth_dependency.py
│   │   └── database_dependency.py
│   │
│   ├── middlewares/
│   │   └── custom_middleware.py
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   ├── device_model.py
│   │   └── loan_model.py
│   │
│   ├── routes/
│   │   ├── user_routes.py
│   │   ├── device_routes.py
│   │   └── loan_routes.py
│   │
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── device_schema.py
│   │   └── loan_schema.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   ├── device_service.py
│   │   └── loan_service.py
│   │
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── requirements.txt
├── README.md
└── .env
```

---

# Swagger UI

La documentación automática está organizada mediante los siguientes grupos:

* Auth
* Users
* Devices
* Loans

Agregar capturas de pantalla de:

1. Página principal de Swagger.
2. Registro de usuario.
3. Inicio de sesión.
4. Endpoint **GET /users**.
5. Endpoint **POST /devices**.
6. Endpoint **POST /loans**.
7. Endpoint **GET /loans/details**.
8. Endpoint **PATCH /loans/{loan_id}/return**.

```text
docs/
├── swagger-home.png
├── auth-register.png
├── auth-login.png
├── users.png
├── devices.png
├── loans.png
└── return-loan.png
```

---

# Autor

**Juan Noriega**

Proyecto desarrollado como práctica de Backend utilizando FastAPI, SQLAlchemy y JWT para la gestión de usuarios, dispositivos tecnológicos y préstamos.

---

# Licencia

Este proyecto tiene fines académicos y educativos.

```
