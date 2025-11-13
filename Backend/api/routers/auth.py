from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from repository.usuario_repository import UsuarioRepository
from passlib.hash import pbkdf2_sha256
from jose import jwt
from datetime import datetime, timedelta
from models.usuario import Usuario

router = APIRouter()

# Simple JWT settings (for demo/dev). In production read from env vars.
SECRET = "dev-secret-key-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


@router.post("/login")
def login(payload: Dict[str, Any]):
    usuario_field = payload.get('usuario') or payload.get('username') or payload.get('email')
    password = payload.get('password')

    if not usuario_field or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="usuario y password requeridos")

    # buscar por nombre de usuario primero, luego por email
    user = UsuarioRepository.obtener_por_nombre_usuario(usuario_field)
    if not user:
        user = UsuarioRepository.obtener_por_email(usuario_field)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    # verificar password
    try:
        ok = pbkdf2_sha256.verify(password, user.password_hash)
    except Exception:
        ok = False

    if not ok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    now = datetime.utcnow()
    payload_token = {
        "sub": user.nombre_usuario,
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    token = jwt.encode(payload_token, SECRET, algorithm=ALGORITHM)

    user_dict = user.to_dict()
    # remove sensitive fields
    user_dict.pop('password_hash', None)

    return {"token": token, "user": user_dict}
