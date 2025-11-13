# 🎉 API FastAPI Lista para Usar

## ✅ Instalación Completada

Todas las dependencias han sido instaladas correctamente:
- ✅ FastAPI (framework web)
- ✅ Uvicorn (servidor ASGI)
- ✅ Pydantic (validación de datos)
- ✅ Python-jose (autenticación JWT)
- ✅ Bcrypt (hashing de contraseñas)
- ✅ Pytest (testing)

## 🚀 Cómo Iniciar el Servidor

```bash
cd Backend
python main.py
```

El servidor se iniciará en: **http://127.0.0.1:8000**

## 📚 Documentación Automática

FastAPI genera documentación interactiva automáticamente:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🧪 Datos de Prueba

Se han creado datos de prueba:
- **Cliente**: Juan Pérez (ID: 1)
- **Cancha**: Cancha 1 - Fútbol 5 (ID: 1)
- **3 Turnos disponibles** para el 15/11/2025

## 🔄 Endpoint Disponible

### POST /api/turnos/{turno_id}/reservar

Registra una reserva sobre un turno disponible.

**URL de ejemplo:**
```
POST http://127.0.0.1:8000/api/turnos/1/reservar
```

**Request Body:**
```json
{
    "id_cliente": 1,
    "id_usuario_registro": 1
}
```

**Respuesta exitosa (200):**
```json
{
    "id": 1,
    "id_cancha": 1,
    "fecha_hora_inicio": "2025-11-15 10:00:00",
    "fecha_hora_fin": "2025-11-15 11:00:00",
    "estado": "reservado",
    "precio_final": 1500.0,
    "id_cliente": 1,
    "id_usuario_registro": 1,
    "reserva_created_at": "2025-11-10 17:45:00",
    "id_usuario_bloqueo": null,
    "motivo_bloqueo": null
}
```

**Errores posibles:**
- `404`: Turno no existe
- `409`: Turno no disponible o cliente no existe
- `500`: Error interno del servidor

## 🧪 Probar con cURL

```bash
# Reservar un turno
curl -X POST "http://127.0.0.1:8000/api/turnos/1/reservar" \
     -H "Content-Type: application/json" \
     -d '{"id_cliente": 1, "id_usuario_registro": 1}'
```

## 🧪 Probar con Python (requests)

```python
import requests

url = "http://127.0.0.1:8000/api/turnos/1/reservar"
data = {
    "id_cliente": 1,
    "id_usuario_registro": 1
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
```

## 📂 Estructura de Archivos Creados/Modificados

```
Backend/
├── main.py                    # ✅ Servidor FastAPI configurado
├── routes/
│   └── turno_routes.py       # ✅ Endpoints de turnos/reservas
├── services/
│   └── turno_service.py      # ✅ Lógica de negocio
├── repository/
│   ├── cliente_repository.py # ✅ CRUD de clientes
│   └── turno_repository.py   # ✅ CRUD de turnos
├── models/
│   ├── cliente.py            # ✅ Modelo Cliente
│   ├── turno.py              # ✅ Modelo Turno
│   └── ... (14 más)
├── database/
│   └── connection.py         # ✅ Conexión SQLite
├── requirements.txt          # ✅ Actualizado con todas las deps
├── setup_api_test.py         # ✅ Script de preparación
└── database.db               # ✅ Base de datos con datos de prueba
```

## 🎯 Siguiente Paso: Probar la API

1. **Inicia el servidor:**
   ```bash
   python main.py
   ```

2. **Abre el navegador en:**
   http://127.0.0.1:8000/docs

3. **Prueba el endpoint "POST /api/turnos/{turno_id}/reservar":**
   - Click en el endpoint
   - Click en "Try it out"
   - Ingresa `1` en `turno_id`
   - En el body ingresa:
     ```json
     {
       "id_cliente": 1,
       "id_usuario_registro": 1
     }
     ```
   - Click en "Execute"

4. **Verifica la respuesta:**
   - Deberías ver un `200 OK` con el turno actualizado a estado "reservado"

## 🐛 Solución de Problemas

### El servidor no inicia
```bash
# Verifica que las dependencias estén instaladas
pip list | grep fastapi

# Reinstala si es necesario
pip install -r requirements.txt
```

### Puerto en uso
Si el puerto 8000 está ocupado, cámbialo en `main.py`:
```python
uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
```

### Error de importación
Asegúrate de estar en el directorio Backend:
```bash
cd Backend
python main.py
```

## 📝 Notas Importantes

1. **CORS**: Si vas a conectar con un frontend, necesitarás configurar CORS en `main.py`
2. **Autenticación**: Por ahora no hay autenticación, todos los endpoints son públicos
3. **Validaciones**: Las validaciones de negocio están en `TurnoService`
4. **Base de datos**: SQLite es para desarrollo, considera PostgreSQL para producción

## 🎓 Recursos

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Tutorial de FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic](https://docs.pydantic.dev/)

---

**¡Tu API está lista! 🚀**

Para más ayuda, revisa la documentación automática en `/docs` o contacta al equipo.
