# device_systems

## Descripción

device_systems es una API REST desarrollada con FastAPI para la gestión de usuarios, dispositivos tecnológicos y préstamos. Permite crear, consultar, actualizar y eliminar registros mediante operaciones CRUD, aplicando relaciones entre modelos, migraciones controladas con Alembic, consultas con joins, filtros avanzados y manejo de errores.

---

## Tecnologías utilizadas

* Python 3.x
* FastAPI
* Uvicorn
* SQLAlchemy
* Alembic
* Pydantic v2
* SQLite
* Swagger UI / OpenAPI

---

## Instalación de dependencias

Clonar el repositorio:

```bash
git clone https://github.com/juan-sena/device_systems.git
cd device_systems
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Migraciones con Alembic

Inicializar Alembic (ya configurado en el proyecto):

```bash
alembic init alembic
```

Generar una migración:

```bash
alembic revision --autogenerate -m "descripción del cambio"
```

Aplicar migraciones:

```bash
alembic upgrade head
```

Ver historial de migraciones:

```bash
alembic history
```

---

## Ejecutar el servidor

```bash
python -m uvicorn app.main:app --reload
```

Servidor disponible en:

```text
http://127.0.0.1:8000
```

Documentación Swagger:

```text
http://127.0.0.1:8000/docs
```

Documentación Redoc:

```text
http://127.0.0.1:8000/redoc
```

---

## Endpoints

### Users

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | /users | Listar usuarios |
| GET | /users/{user_id} | Obtener usuario por ID |
| POST | /users | Crear usuario |
| PUT | /users/{user_id} | Actualizar usuario completo |
| PATCH | /users/{user_id} | Actualización parcial |
| DELETE | /users/{user_id} | Eliminar usuario |
| GET | /users/{user_id}/loans | Préstamos de un usuario |

### Devices

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | /devices | Listar dispositivos (con filtros) |
| GET | /devices/{device_id} | Obtener dispositivo por ID |
| POST | /devices | Crear dispositivo |
| PUT | /devices/{device_id} | Actualizar dispositivo completo |
| PATCH | /devices/{device_id} | Actualización parcial |
| DELETE | /devices/{device_id} | Eliminar dispositivo |
| GET | /devices/{device_id}/loans | Historial de préstamos del dispositivo |

### Loans

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | /loans | Listar préstamos (con filtros) |
| GET | /loans/details | Listar préstamos con detalles |
| GET | /loans/{loan_id} | Obtener préstamo por ID |
| POST | /loans | Crear préstamo |
| PATCH | /loans/{loan_id}/return | Devolver dispositivo |

### Filtros disponibles

**Dispositivos:**
- `GET /devices?device_type=laptop`
- `GET /devices?is_available=true`
- `GET /devices?brand=lenovo`
- `GET /devices?search=thinkpad`

**Préstamos:**
- `GET /loans?status=active`
- `GET /loans?user_email=ana@sena.edu.co`
- `GET /loans?device_type=laptop`

---

## Ejemplos de peticiones y respuestas

### Crear usuario

**POST /users**

Petición:

```json
{
  "name": "Ana Pérez",
  "email": "ana@sena.edu.co",
  "role": "user"
}
```

Respuesta:

```json
{
  "id": 1,
  "name": "Ana Pérez",
  "email": "ana@sena.edu.co",
  "role": "user",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00"
}
```

---

### Crear dispositivo

**POST /devices**

Petición:

```json
{
  "name": "Laptop Lenovo ThinkPad",
  "serial_number": "LEN-2024-001",
  "device_type": "laptop",
  "brand": "Lenovo"
}
```

Respuesta:

```json
{
  "id": 1,
  "name": "Laptop Lenovo ThinkPad",
  "serial_number": "LEN-2024-001",
  "device_type": "laptop",
  "brand": "Lenovo",
  "is_available": true,
  "created_at": "2024-01-15T10:30:00"
}
```

---

### Crear préstamo

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
  "loan_date": "2024-01-15T10:30:00",
  "return_date": null,
  "status": "active",
  "user": {
    "id": 1,
    "name": "Ana Pérez",
    "email": "ana@sena.edu.co"
  },
  "device": {
    "id": 1,
    "name": "Laptop Lenovo ThinkPad",
    "serial_number": "LEN-2024-001",
    "device_type": "laptop"
  }
}
```

---

### Devolver dispositivo

**PATCH /loans/1/return**

Respuesta:

```json
{
  "id": 1,
  "loan_date": "2024-01-15T10:30:00",
  "return_date": "2024-01-20T14:00:00",
  "status": "returned",
  "user": {
    "id": 1,
    "name": "Ana Pérez",
    "email": "ana@sena.edu.co"
  },
  "device": {
    "id": 1,
    "name": "Laptop Lenovo ThinkPad",
    "serial_number": "LEN-2024-001",
    "device_type": "laptop"
  }
}
```

---

### Consultar préstamos con filtros

**GET /loans?status=active**

Respuesta:

```json
[
  {
    "id": 1,
    "loan_date": "2024-01-15T10:30:00",
    "return_date": null,
    "status": "active",
    "user": {
      "id": 1,
      "name": "Ana Pérez",
      "email": "ana@sena.edu.co"
    },
    "device": {
      "id": 1,
      "name": "Laptop Lenovo ThinkPad",
      "serial_number": "LEN-2024-001",
      "device_type": "laptop"
    }
  }
]
```

---

## Códigos de estado HTTP utilizados

| Código | Descripción |
| ------ | ----------- |
| 200 OK | Operación exitosa |
| 201 Created | Recurso creado correctamente |
| 204 No Content | Eliminación exitosa |
| 400 Bad Request | Dato duplicado o datos inválidos |
| 404 Not Found | Recurso no encontrado |
| 409 Conflict | Regla de negocio incumplida |
| 422 Unprocessable Entity | Error de validación de datos |

---

## Manejo de errores

### Recurso no encontrado

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

Código HTTP: `404 Not Found`

### Dato duplicado

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

Código HTTP: `400 Bad Request`

### Regla de negocio

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

Código HTTP: `409 Conflict`

### Error de validación

Código HTTP: `422 Unprocessable Entity`

---

## Estructura del proyecto

```
device_systems/
│── app/
│ │── main.py
│ │── database/
│ │ │── connection.py
│ │── models/
│ │ │── user_model.py
│ │ │── device_model.py
│ │ │── loan_model.py
│ │── schemas/
│ │ │── user_schema.py
│ │ │── device_schema.py
│ │ │── loan_schema.py
│ │── routes/
│ │ │── user_routes.py
│ │ │── device_routes.py
│ │ │── loan_routes.py
│ │── services/
│ │ │── user_service.py
│ │ │── device_service.py
│ │ │── loan_service.py
│ │── dependencies/
│ │ │── database_dependency.py
│
│── alembic/
│ │── versions/
│── alembic.ini
│── requirements.txt
│── README.md
```

---

## Swagger UI

La documentación automática está organizada por tags:
- **Users**
- **Devices**
- **Loans**

Agregar capturas de pantalla de:

1. Página principal de Swagger.
2. Endpoint GET /users.
3. Endpoint POST /devices.
4. Endpoint POST /loans.
5. Endpoint GET /loans/details.
6. Endpoint PATCH /loans/{loan_id}/return.

![Swagger Principal](docs/swagger-home.png)
