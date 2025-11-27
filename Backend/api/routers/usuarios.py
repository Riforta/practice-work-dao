from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Optional

from api.dependencies.auth import require_admin, require_role
from models.usuario import Usuario
from services import usuarios_service, clientes_service
from services.auth_service import AuthService

router = APIRouter()


@router.post("/usuarios/register", status_code=status.HTTP_201_CREATED)
def registrar_usuario_cliente(payload: Dict[str, Any]):
    """
    Registra un nuevo usuario y su perfil de cliente en el sistema.
    Devuelve un token JWT para auto-login.
    
    Este endpoint orquesta la creación de Usuario, Cliente y generación de token,
    usando sus respectivos servicios para mantener alta cohesión y bajo acoplamiento.
    
    Body esperado:
    {
        // Datos de Usuario
        "nombre_usuario": "juanperez",
        "email": "juan@example.com",
        "password": "password123",
        "id_rol": 2,  // Opcional, default 2 (Cliente)
        
        // Datos de Cliente
        "nombre": "Juan",
        "apellido": "Pérez",
        "dni": "12345678",
        "telefono": "1234567890",  // Opcional
        "direccion": "Calle Falsa 123"  // Opcional
    }
    
    Returns:
        - **token**: Token JWT para usar inmediatamente (auto-login)
        - **user**: Datos básicos del usuario creado
        - **cliente**: Datos básicos del cliente creado
        - **message**: Mensaje de confirmación
    """
    try:
        # 1. Preparar datos de usuario
        usuario_data = {
            'nombre_usuario': payload.get('nombre_usuario'),
            'email': payload.get('email'),
            'password': payload.get('password'),
            'id_rol': payload.get('id_rol', 2)  # Default: Cliente
        }

        # 3. Preparar datos de cliente vinculado al usuario
        cliente_data = {
            'id_usuario': usuario.id,  # Vincular con usuario recién creado
            'nombre': payload.get('nombre'),
            'apellido': payload.get('apellido'),
            'dni': payload.get('dni'),
            'telefono': payload.get('telefono'),
        }
        
        # 2. Registrar usuario (usuarios_service)
        usuario, cliente, token = usuarios_service.registrar_usuario(usuario_data, cliente_data) 
        
        # 6. Preparar respuesta usando to_dict()
        user_dict = usuario.to_dict()
        user_dict.pop('password', None)  # Nunca exponer password_hash
        
        return {
            "token": token,
            "user": user_dict,
            "cliente": cliente.to_dict(),
            "message": "Usuario y cliente registrados exitosamente"
        }
        
    except ValueError as e:
        # Errores de validación de usuario o cliente
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Otros errores
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usuarios/", response_model=List[Dict[str, Any]])
def listar_usuarios(admin_check: Usuario = Depends(require_admin)):
    items = usuarios_service.listar_usuarios()
    results = []
    for i in items:
        d = i.to_dict()
        d.pop('password_hash', None)
        results.append(d)
    return results


@router.get("/usuarios/{usuario_id}", response_model=Dict[str, Any])
def obtener_usuario(usuario_id: int, admin_check: Usuario = Depends(require_admin)):
    try:
        u = usuarios_service.obtener_usuario_por_id(usuario_id)
        d = u.to_dict()
        d.pop('password_hash', None)
        return d
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/usuarios/{usuario_id}", response_model=Dict[str, Any])
def actualizar_usuario(usuario_id: int, payload: Dict[str, Any],
                    admin_check: Usuario = Depends(require_admin),
                    current_user: Usuario = Depends(require_role("cliente"))):
    try:
        u = usuarios_service.actualizar_usuario(usuario_id, payload)
        return u.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int, current_user: Usuario = Depends(require_role("cliente")),
                    admin_check: Usuario = Depends(require_admin)):
    try:
        usuarios_service.eliminar_usuario(usuario_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
