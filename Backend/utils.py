"""
Utilidades generales para el proyecto.
"""

from datetime import datetime, timedelta
from typing import Optional
import re


def validar_email(email: str) -> bool:
    """
    Valida el formato de un email.
    
    Args:
        email: String del email a validar
        
    Returns:
        True si el email es válido, False en caso contrario
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validar_telefono_argentino(telefono: str) -> bool:
    """
    Valida el formato de un teléfono argentino.
    Acepta formatos: 351-1234567, 3511234567, +54 351 1234567, etc.
    
    Args:
        telefono: String del teléfono a validar
        
    Returns:
        True si el teléfono es válido, False en caso contrario
    """
    if not telefono:
        return False
    
    # Remover espacios, guiones y paréntesis
    telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono)
    
    # Remover prefijo internacional
    telefono_limpio = telefono_limpio.lstrip('+549').lstrip('549')
    
    # Debe tener entre 7 y 10 dígitos
    return telefono_limpio.isdigit() and 7 <= len(telefono_limpio) <= 10


def validar_dni(dni: str) -> bool:
    """
    Valida el formato de un DNI argentino.
    
    Args:
        dni: String del DNI a validar
        
    Returns:
        True si el DNI es válido, False en caso contrario
    """
    if not dni:
        return False
    
    # Remover puntos y espacios
    dni_limpio = dni.replace('.', '').replace(' ', '')
    
    # Debe ser numérico y tener entre 7 y 8 dígitos
    return dni_limpio.isdigit() and 7 <= len(dni_limpio) <= 8


def formatear_fecha_hora(fecha_str: str, formato_entrada: str = '%Y-%m-%d %H:%M:%S') -> Optional[datetime]:
    """
    Convierte un string de fecha a objeto datetime.
    
    Args:
        fecha_str: String de la fecha
        formato_entrada: Formato del string de entrada
        
    Returns:
        Objeto datetime o None si hay error
    """
    try:
        return datetime.strptime(fecha_str, formato_entrada)
    except (ValueError, TypeError):
        return None


def obtener_fecha_hora_actual() -> str:
    """
    Obtiene la fecha y hora actual en formato SQLite.
    
    Returns:
        String con la fecha y hora actual
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def calcular_duracion_turno(fecha_inicio: str, fecha_fin: str) -> Optional[float]:
    """
    Calcula la duración de un turno en horas.
    
    Args:
        fecha_inicio: Fecha y hora de inicio
        fecha_fin: Fecha y hora de fin
        
    Returns:
        Duración en horas o None si hay error
    """
    inicio = formatear_fecha_hora(fecha_inicio)
    fin = formatear_fecha_hora(fecha_fin)
    
    if inicio and fin:
        duracion = fin - inicio
        return duracion.total_seconds() / 3600
    
    return None


def calcular_precio_turno(precio_por_hora: float, duracion_horas: float) -> float:
    """
    Calcula el precio de un turno basado en la duración.
    
    Args:
        precio_por_hora: Precio por hora de la cancha
        duracion_horas: Duración del turno en horas
        
    Returns:
        Precio total del turno
    """
    return round(precio_por_hora * duracion_horas, 2)


def generar_horarios_disponibles(fecha: str, hora_inicio: int = 8, hora_fin: int = 23, 
                                 duracion_turno: int = 60) -> list:
    """
    Genera una lista de horarios disponibles para un día.
    
    Args:
        fecha: Fecha en formato 'YYYY-MM-DD'
        hora_inicio: Hora de inicio (0-23)
        hora_fin: Hora de fin (0-23)
        duracion_turno: Duración de cada turno en minutos
        
    Returns:
        Lista de tuplas (fecha_hora_inicio, fecha_hora_fin)
    """
    horarios = []
    hora_actual = hora_inicio
    
    while hora_actual < hora_fin:
        inicio = datetime.strptime(f"{fecha} {hora_actual:02d}:00:00", '%Y-%m-%d %H:%M:%S')
        fin = inicio + timedelta(minutes=duracion_turno)
        
        horarios.append((
            inicio.strftime('%Y-%m-%d %H:%M:%S'),
            fin.strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        hora_actual += duracion_turno // 60
    
    return horarios


def formatear_precio(precio: float, moneda: str = '$') -> str:
    """
    Formatea un precio para mostrar.
    
    Args:
        precio: Precio a formatear
        moneda: Símbolo de la moneda
        
    Returns:
        String con el precio formateado
    """
    return f"{moneda} {precio:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def truncar_texto(texto: str, longitud: int = 50, sufijo: str = '...') -> str:
    """
    Trunca un texto a una longitud específica.
    
    Args:
        texto: Texto a truncar
        longitud: Longitud máxima
        sufijo: Sufijo a agregar si se trunca
        
    Returns:
        Texto truncado
    """
    if len(texto) <= longitud:
        return texto
    return texto[:longitud - len(sufijo)] + sufijo


# Constantes útiles
ESTADOS_TURNO = {
    'DISPONIBLE': 'disponible',
    'RESERVADO': 'reservado',
    'BLOQUEADO': 'bloqueado',
    'CANCELADO': 'cancelado',
    'COMPLETADO': 'completado'
}

ESTADOS_PEDIDO = {
    'PENDIENTE': 'pendiente_pago',
    'PAGADO': 'pagado',
    'CANCELADO': 'cancelado',
    'VENCIDO': 'vencido'
}

ESTADOS_PAGO = {
    'INICIADO': 'iniciado',
    'PROCESANDO': 'procesando',
    'APROBADO': 'aprobado',
    'RECHAZADO': 'rechazado',
    'CANCELADO': 'cancelado'
}

ESTADOS_TORNEO = {
    'PLANIFICADO': 'planificado',
    'INSCRIPCION': 'inscripcion_abierta',
    'EN_CURSO': 'en_curso',
    'FINALIZADO': 'finalizado',
    'CANCELADO': 'cancelado'
}


if __name__ == "__main__":
    # Pruebas de las funciones
    print("🧪 Probando utilidades...\n")
    
    # Validaciones
    print("✓ Email válido:", validar_email("test@example.com"))
    print("✓ Email inválido:", validar_email("test@"))
    print("✓ Teléfono válido:", validar_telefono_argentino("351-1234567"))
    print("✓ DNI válido:", validar_dni("12345678"))
    
    # Fechas
    print("\n✓ Fecha actual:", obtener_fecha_hora_actual())
    
    # Horarios disponibles
    horarios = generar_horarios_disponibles("2025-11-15", 8, 12, 60)
    print(f"\n✓ Horarios generados: {len(horarios)}")
    for inicio, fin in horarios[:3]:
        print(f"  - {inicio} a {fin}")
    
    # Formato de precio
    print("\n✓ Precio formateado:", formatear_precio(1500.50))
    
    print("\n✅ Todas las utilidades funcionan correctamente")
