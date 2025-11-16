import sys
import os

# Ensure the package root (the Backend folder) is on sys.path so imports like
# 'services.usuarios_services' resolve when running this script directly.
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Backend.services.usuarios_service import crear_usuario


if __name__ == '__main__':
    payload = {
        'username': 'testuser2',
        'email': 'testuser2@example.com',
        'password': 'TestPass123'
    }
    try:
        u = crear_usuario(payload)
        print('Usuario creado:', u.to_dict())
    except Exception as e:
        print('Error:', e)
