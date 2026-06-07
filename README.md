# device_systems

## Descripción

device_systems es una API REST desarrollada con FastAPI para la gestión de usuarios. Permite crear, consultar, actualizar y eliminar usuarios mediante operaciones CRUD, aplicando validaciones, manejo de errores, documentación automática y dependencias reutilizables con Depends().

---

## Tecnologías utilizadas

* Python 3.x
* FastAPI
* Uvicorn
* Pydantic
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
pip install fastapi uvicorn pydantic email-validator
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

---

## Endpoints

| Método | Endpoint         | Descripción                 |
| ------ | ---------------- | --------------------------- |
| GET    | /users           | Listar usuarios             |
| GET    | /users/{user_id} | Obtener usuario por ID      |
| POST   | /users           | Crear usuario               |
| PUT    | /users/{user_id} | Actualizar usuario completo |
| PATCH  | /users/{user_id} | Actualización parcial       |
| DELETE | /users/{user_id} | Eliminar usuario            |

---

## Ejemplos de peticiones y respuestas

### Crear usuario

**POST /users**

Petición:

```json
{
  "id": 1,
  "name": "Juan",
  "email": "juan@gmail.com",
  "role": "user",
  "is_active": true
}
```

Respuesta:

```json
{
  "id": 1,
  "name": "Juan",
  "role": "user"
}
```

---

### Obtener usuario por ID

**GET /users/1**

Respuesta:

```json
{
  "id": 1,
  "name": "Juan",
  "email": "juan@gmail.com",
  "role": "user",
  "is_active": true
}
```

---

### Actualización parcial

**PATCH /users/1**

Petición:

```json
{
  "role": "support"
}
```

Respuesta:

```json
{
  "id": 1,
  "name": "Juan",
  "email": "juan@gmail.com",
  "role": "support",
  "is_active": true
}
```

---

### Eliminar usuario

**DELETE /users/1**

Respuesta:

```json
{
  "message": "Usuario eliminado exitosamente"
}
```

---

## Códigos de estado HTTP utilizados

| Código                   | Descripción                        |
| ------------------------ | ---------------------------------- |
| 200 OK                   | Operación exitosa                  |
| 201 Created              | Recurso creado correctamente       |
| 400 Bad Request          | Datos inválidos o correo duplicado |
| 404 Not Found            | Usuario no encontrado              |
| 422 Unprocessable Entity | Error de validación de datos       |

---

## Swagger UI

Agregar capturas de pantalla de:

1. Página principal de Swagger.
2. Endpoint GET /users.
3. Endpoint POST /users.
4. Endpoint PATCH /users/{user_id}.
5. Endpoint DELETE /users/{user_id}.

Ejemplo:

![Swagger Principal](docs/swagger-home.png)

![Swagger Users](docs/swagger-users.png)

---

## Uso de Depends()

Se implementó Dependency Injection mediante Depends() para reutilizar lógica dentro de la API.

Se creó la dependencia:

```python
def get_user_or_404(user_id: int):
```

Esta función busca un usuario por ID y retorna un error 404 cuando no existe.

Posteriormente fue utilizada en las rutas mediante:

```python
usuario = Depends(get_user_or_404)
```

Esto permite reutilizar código y mejorar la mantenibilidad de la aplicación.

---

## Manejo de errores

La API implementa manejo de errores mediante HTTPException.

### Usuario no encontrado

```json
{
  "detail": "Usuario no encontrado"
}
```

Código HTTP:

```text
404 Not Found
```

### Correo duplicado

```json
{
  "detail": "El correo ya existe"
}
```

Código HTTP:

```text
400 Bad Request
```

### Actualización sin datos

```json
{
  "detail": "Debe enviar al menos un campo para actualizar"
}
```

Código HTTP:

```text
400 Bad Request
```

### Error de validación

```text
422 Unprocessable Entity
```

Generado automáticamente por Pydantic cuando los datos enviados no cumplen las reglas definidas en los esquemas.
