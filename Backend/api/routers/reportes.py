"""
Router para endpoints de reportes y estadísticas.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, Dict, Any, List
from datetime import datetime

from services.reportes_service import ReportesService
from api.dependencies.auth import require_admin
from models.usuario import Usuario

router = APIRouter()


@router.get("/reportes/resumen", response_model=Dict[str, Any])
def obtener_resumen_general(
    current_user: Usuario = Depends(require_admin)
):
    """
    Obtiene un resumen general con métricas principales del sistema.
    """
    try:
        resumen = ReportesService.resumen_general()
        return resumen
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reportes/reservas-por-cliente", response_model=List[Dict[str, Any]])
def obtener_reservas_por_cliente(
    id_cliente: Optional[int] = Query(None, description="ID del cliente (opcional)"),
    current_user: Usuario = Depends(require_admin)
):
    """
    Lista todas las reservas agrupadas por cliente.
    Si se proporciona id_cliente, filtra solo ese cliente.
    """
    try:
        reportes = ReportesService.listado_reservas_por_cliente(id_cliente=id_cliente)
        return reportes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reportes/reservas-por-cancha", response_model=List[Dict[str, Any]])
def obtener_reservas_por_cancha(
    fecha_inicio: str = Query(..., description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: str = Query(..., description="Fecha fin (YYYY-MM-DD)"),
    id_cancha: Optional[int] = Query(None, description="ID de cancha específica (opcional)"),
    current_user: Usuario = Depends(require_admin)
):
    """
    Lista reservas por cancha en un período específico.
    """
    try:
        # Validar formato de fechas
        try:
            datetime.fromisoformat(fecha_inicio)
            datetime.fromisoformat(fecha_fin)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Formato de fecha inválido. Use YYYY-MM-DD"
            )
        
        reportes = ReportesService.reservas_por_cancha_periodo(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            id_cancha=id_cancha
        )
        return reportes
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reportes/canchas-mas-utilizadas", response_model=List[Dict[str, Any]])
def obtener_canchas_mas_utilizadas(
    limite: int = Query(10, ge=1, le=50, description="Cantidad máxima de canchas"),
    current_user: Usuario = Depends(require_admin)
):
    """
    Retorna las canchas más utilizadas ordenadas por cantidad de reservas.
    """
    try:
        reportes = ReportesService.canchas_mas_utilizadas(limite=limite)
        return reportes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reportes/utilizacion-mensual", response_model=List[Dict[str, Any]])
def obtener_utilizacion_mensual(
    anio: Optional[int] = Query(None, ge=2000, le=2100, description="Año (opcional, default: actual)"),
    current_user: Usuario = Depends(require_admin)
):
    """
    Retorna estadísticas de utilización mensual de canchas.
    Si no se proporciona año, usa el año actual.
    """
    try:
        reportes = ReportesService.utilizacion_mensual_canchas(anio=anio)
        return reportes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
