"""
Servicio de reportes para estadísticas y análisis del sistema.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from repositories.turno_repository import TurnoRepository
from repositories.cancha_repository import CanchaRepository
from repositories.cliente_repository import ClienteRepository
from repositories.pago_repository import PagoRepository
from repositories.turno_servicio_repository import TurnoXServicioRepository


class ReportesService:
    """Servicio para generar reportes y estadísticas"""

    @staticmethod
    def listado_reservas_por_cliente(id_cliente: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Lista todas las reservas agrupadas por cliente.
        Si se proporciona id_cliente, filtra solo ese cliente.
        
        Returns:
            Lista de diccionarios con información de reservas por cliente
        """
        # Obtener todos los turnos reservados y completados
        turnos_reservados = TurnoRepository.obtener_todos_filtrados(
            estado='reservado',
            id_cliente=id_cliente
        )
        turnos_completados = TurnoRepository.obtener_todos_filtrados(
            estado='completado',
            id_cliente=id_cliente
        )
        
        # Combinar ambas listas
        turnos = turnos_reservados + turnos_completados
        
        # Agrupar por cliente
        reservas_por_cliente: Dict[int, List[Dict[str, Any]]] = {}
        
        for turno in turnos:
            if turno.id_cliente:
                if turno.id_cliente not in reservas_por_cliente:
                    reservas_por_cliente[turno.id_cliente] = []
                
                # Obtener información de la cancha
                cancha = CanchaRepository.obtener_por_id(turno.id_cancha)
                cancha_nombre = cancha.nombre if cancha else f"Cancha {turno.id_cancha}"
                
                # Calcular total de servicios adicionales
                monto_servicios = TurnoXServicioRepository.calcular_total_servicios(turno.id)
                total = turno.precio_final + monto_servicios
                
                reservas_por_cliente[turno.id_cliente].append({
                    'id_turno': turno.id,
                    'cancha': cancha_nombre,
                    'fecha_hora_inicio': turno.fecha_hora_inicio,
                    'fecha_hora_fin': turno.fecha_hora_fin,
                    'precio_final': turno.precio_final,
                    'monto_servicios': monto_servicios,
                    'total': total,
                    'reserva_created_at': turno.reserva_created_at
                })
        
        # Construir resultado con información del cliente
        resultado = []
        for id_cliente, reservas in reservas_por_cliente.items():
            cliente = ClienteRepository.obtener_por_id(id_cliente)
            if cliente:
                # Calcular totales
                total_gastado = sum(r['total'] for r in reservas)
                total_servicios = sum(r['monto_servicios'] for r in reservas)
                
                resultado.append({
                    'id_cliente': id_cliente,
                    'nombre_cliente': f"{cliente.nombre} {cliente.apellido or ''}".strip(),
                    'dni': cliente.dni,
                    'telefono': cliente.telefono,
                    'cantidad_reservas': len(reservas),
                    'total_gastado': total_gastado,
                    'total_servicios': total_servicios,
                    'reservas': sorted(reservas, key=lambda x: x['fecha_hora_inicio'], reverse=True)
                })
        
        return sorted(resultado, key=lambda x: x['cantidad_reservas'], reverse=True)

    @staticmethod
    def reservas_por_cancha_periodo(
        fecha_inicio: str,
        fecha_fin: str,
        id_cancha: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Lista reservas por cancha en un período específico.
        
        Args:
            fecha_inicio: Fecha inicial en formato ISO (YYYY-MM-DD)
            fecha_fin: Fecha final en formato ISO (YYYY-MM-DD)
            id_cancha: ID de cancha específica (opcional)
        
        Returns:
            Lista de diccionarios con reservas agrupadas por cancha
        """
        # Obtener todos los turnos reservados y completados
        turnos_reservados = TurnoRepository.obtener_todos_filtrados(
            estado='reservado',
            id_cancha=id_cancha
        )
        turnos_completados = TurnoRepository.obtener_todos_filtrados(
            estado='completado',
            id_cancha=id_cancha
        )
        
        # Combinar ambas listas
        turnos = turnos_reservados + turnos_completados
        
        # Filtrar por fecha
        fecha_inicio_dt = datetime.fromisoformat(fecha_inicio)
        fecha_fin_dt = datetime.fromisoformat(fecha_fin)
        
        turnos_filtrados = []
        for turno in turnos:
            try:
                turno_fecha = datetime.fromisoformat(turno.fecha_hora_inicio.split()[0])
                if fecha_inicio_dt <= turno_fecha <= fecha_fin_dt:
                    turnos_filtrados.append(turno)
            except:
                continue
        
        # Agrupar por cancha
        reservas_por_cancha: Dict[int, List[Dict[str, Any]]] = {}
        
        for turno in turnos_filtrados:
            if turno.id_cancha not in reservas_por_cancha:
                reservas_por_cancha[turno.id_cancha] = []
            
            # Obtener información del cliente
            cliente_nombre = "Sin información"
            if turno.id_cliente:
                cliente = ClienteRepository.obtener_por_id(turno.id_cliente)
                if cliente:
                    cliente_nombre = f"{cliente.nombre} {cliente.apellido or ''}".strip()
            
            reservas_por_cancha[turno.id_cancha].append({
                'id_turno': turno.id,
                'fecha_hora_inicio': turno.fecha_hora_inicio,
                'fecha_hora_fin': turno.fecha_hora_fin,
                'cliente': cliente_nombre,
                'precio_final': turno.precio_final
            })
        
        # Construir resultado con información de la cancha
        resultado = []
        for id_cancha, reservas in reservas_por_cancha.items():
            cancha = CanchaRepository.obtener_por_id(id_cancha)
            if cancha:
                ingresos_totales = sum(r['precio_final'] for r in reservas)
                resultado.append({
                    'id_cancha': id_cancha,
                    'nombre_cancha': cancha.nombre,
                    'tipo_cancha': cancha.tipo_deporte or 'Sin especificar',
                    'cantidad_reservas': len(reservas),
                    'ingresos_totales': ingresos_totales,
                    'reservas': sorted(reservas, key=lambda x: x['fecha_hora_inicio'])
                })
        
        return sorted(resultado, key=lambda x: x['cantidad_reservas'], reverse=True)

    @staticmethod
    def canchas_mas_utilizadas(limite: int = 10) -> List[Dict[str, Any]]:
        """
        Retorna las canchas más utilizadas ordenadas por cantidad de reservas.
        
        Args:
            limite: Cantidad máxima de canchas a retornar
        
        Returns:
            Lista de diccionarios con estadísticas de cada cancha
        """
        # Obtener todas las reservas (reservadas y completadas)
        turnos_reservados = TurnoRepository.obtener_todos_filtrados(estado='reservado')
        turnos_completados = TurnoRepository.obtener_todos_filtrados(estado='completado')
        todos_turnos = turnos_reservados + turnos_completados
        
        # Contar reservas por cancha
        conteo_por_cancha: Dict[int, int] = {}
        ingresos_por_cancha: Dict[int, float] = {}
        
        for turno in todos_turnos:
            conteo_por_cancha[turno.id_cancha] = conteo_por_cancha.get(turno.id_cancha, 0) + 1
            ingresos_por_cancha[turno.id_cancha] = ingresos_por_cancha.get(turno.id_cancha, 0) + turno.precio_final
        
        # Construir resultado con información de la cancha
        resultado = []
        for id_cancha, cantidad in conteo_por_cancha.items():
            cancha = CanchaRepository.obtener_por_id(id_cancha)
            if cancha:
                resultado.append({
                    'id_cancha': id_cancha,
                    'nombre_cancha': cancha.nombre,
                    'tipo_cancha': cancha.tipo_deporte or 'Sin especificar',
                    'cantidad_reservas': cantidad,
                    'ingresos_totales': ingresos_por_cancha.get(id_cancha, 0),
                    'precio_promedio': ingresos_por_cancha.get(id_cancha, 0) / cantidad if cantidad > 0 else 0
                })
        
        # Ordenar por cantidad de reservas
        resultado_ordenado = sorted(resultado, key=lambda x: x['cantidad_reservas'], reverse=True)
        
        return resultado_ordenado[:limite]

    @staticmethod
    def utilizacion_mensual_canchas(anio: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retorna estadísticas de utilización mensual de canchas.
        Si no se proporciona año, usa el año actual.
        
        Args:
            anio: Año para el reporte (opcional, por defecto año actual)
        
        Returns:
            Lista de diccionarios con utilización por mes y cancha
        """
        if anio is None:
            anio = datetime.now().year
        
        # Obtener todas las reservas del año (reservadas y completadas)
        turnos_reservados = TurnoRepository.obtener_todos_filtrados(estado='reservado')
        turnos_completados = TurnoRepository.obtener_todos_filtrados(estado='completado')
        
        # Combinar ambas listas
        todos_turnos = turnos_reservados + turnos_completados
        
        # Filtrar por año
        turnos_anio = []
        for turno in todos_turnos:
            try:
                fecha_turno = datetime.fromisoformat(turno.fecha_hora_inicio)
                if fecha_turno.year == anio:
                    turnos_anio.append(turno)
            except:
                continue
        
        # Estructura: {mes: {id_cancha: cantidad}}
        utilizacion: Dict[int, Dict[int, int]] = {}
        ingresos: Dict[int, Dict[int, float]] = {}
        
        for turno in turnos_anio:
            try:
                fecha_turno = datetime.fromisoformat(turno.fecha_hora_inicio)
                mes = fecha_turno.month
                
                if mes not in utilizacion:
                    utilizacion[mes] = {}
                    ingresos[mes] = {}
                
                if turno.id_cancha not in utilizacion[mes]:
                    utilizacion[mes][turno.id_cancha] = 0
                    ingresos[mes][turno.id_cancha] = 0
                
                # Calcular servicios adicionales
                monto_servicios = TurnoXServicioRepository.calcular_total_servicios(turno.id)
                total_turno = turno.precio_final + monto_servicios
                
                utilizacion[mes][turno.id_cancha] += 1
                ingresos[mes][turno.id_cancha] += total_turno
            except:
                continue
        
        # Obtener información de todas las canchas
        todas_canchas = CanchaRepository.listar_todas()
        canchas_info = {c.id: c.nombre for c in todas_canchas if c.id}
        
        # Construir resultado
        meses_nombres = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        
        resultado = []
        for mes in range(1, 13):
            datos_mes = {
                'mes': mes,
                'nombre_mes': meses_nombres[mes - 1],
                'anio': anio,
                'total_reservas': sum(utilizacion.get(mes, {}).values()),
                'ingresos_totales': sum(ingresos.get(mes, {}).values()),
                'canchas': []
            }
            
            # Agregar datos por cancha
            if mes in utilizacion:
                for id_cancha, cantidad in utilizacion[mes].items():
                    datos_mes['canchas'].append({
                        'id_cancha': id_cancha,
                        'nombre_cancha': canchas_info.get(id_cancha, f'Cancha {id_cancha}'),
                        'cantidad_reservas': cantidad,
                        'ingresos': ingresos[mes].get(id_cancha, 0)
                    })
                
                # Ordenar canchas por cantidad de reservas
                datos_mes['canchas'] = sorted(
                    datos_mes['canchas'],
                    key=lambda x: x['cantidad_reservas'],
                    reverse=True
                )
            
            resultado.append(datos_mes)
        
        return resultado

    @staticmethod
    def resumen_general() -> Dict[str, Any]:
        """
        Retorna un resumen general del sistema con métricas principales.
        
        Returns:
            Diccionario con métricas generales del sistema
        """
        # Obtener datos
        todas_canchas = CanchaRepository.listar_todas()
        todos_clientes = ClienteRepository.listar_todos()
        turnos_reservados = TurnoRepository.obtener_todos_filtrados(estado='reservado')
        turnos_completados = TurnoRepository.obtener_todos_filtrados(estado='completado')
        todos_turnos = turnos_reservados + turnos_completados
        todos_pagos = PagoRepository.listar_todos()
        
        # Calcular métricas
        total_ingresos = sum(p.monto_total for p in todos_pagos if p.estado == 'completado')
        total_reservas = len(todos_turnos)
        
        # Clientes activos (con al menos una reserva)
        clientes_con_reserva = set(t.id_cliente for t in todos_turnos if t.id_cliente)
        
        return {
            'total_canchas': len(todas_canchas),
            'total_clientes': len(todos_clientes),
            'clientes_activos': len(clientes_con_reserva),
            'total_reservas': total_reservas,
            'total_ingresos': total_ingresos,
            'ingreso_promedio_por_reserva': total_ingresos / total_reservas if total_reservas > 0 else 0,
            'fecha_generacion': datetime.now().isoformat()
        }
