# device_systems

API desarrollada con FastAPI para gestionar usuarios.

## Tecnologías
- Python
- FastAPI
- Pydantic

---

# Instalación

```bash
pip install -r requirements.txt
```

---

# Ejecutar servidor

```bash
uvicorn app.main:app --reload
```

---

# Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

# Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| GET | /users | Listar usuarios |
| GET | /users/{user_id} | Buscar usuario por ID |
| POST | /users | Crear usuario |

---

# Ejemplo GET

```text
/users?role=admin
```

---

# Ejemplo POST

```json
{
  "id": 1,
  "name": "Juan",
  "email": "juan@gmail.com",
  "role": "admin",
  "is_active": true
}
```

---

# Headers personalizados

```text
X-App-Name: device_systems
X-API-Version: 1.0
```

---

# Capturas Swagger

Agregar imágenes aquí.