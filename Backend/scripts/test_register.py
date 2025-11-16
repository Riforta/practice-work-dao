from Backend.services.usuarios_service import crear_usuario

if __name__ == '__main__':
    payload = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'TestPass123'
    }
    try:
        u = crear_usuario(payload)
        print('Usuario creado:', u.to_dict())
    except Exception as e:
        print('Error:', e)
