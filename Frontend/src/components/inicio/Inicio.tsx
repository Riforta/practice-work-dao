import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useModal } from '../../contexts/ModalContext';
import reportesService from '../../services/reportes.service';
import type { ResumenGeneral, CanchaMasUtilizada } from '../../services/reportes.service';
import { 
  UsersIcon, 
  CalendarIcon, 
  CurrencyDollarIcon,
  TrophyIcon,
  Squares2X2Icon,
  ChartBarIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
  UserGroupIcon
} from '@heroicons/react/24/outline';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  subtitle?: string;
  trend?: string;
}

function StatCard({ title, value, icon, subtitle, trend }: StatCardProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <div className="text-gray-500 dark:text-gray-400">{icon}</div>
        {trend && (
          <span className="text-sm font-medium text-green-600 dark:text-green-400">
            {trend}
          </span>
        )}
      </div>
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
        {value}
      </h3>
      <p className="text-sm text-gray-600 dark:text-gray-300">{title}</p>
      {subtitle && (
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">{subtitle}</p>
      )}
    </div>
  );
}

export default function Inicio() {
  const { user } = useAuth();
  const { openModal } = useModal();
  const navigate = useNavigate();
  const [resumen, setResumen] = useState<ResumenGeneral | null>(null);
  const [topCanchas, setTopCanchas] = useState<CanchaMasUtilizada[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const isAdmin = user?.id_rol === 1;

  useEffect(() => {
    // Solo cargar datos del dashboard si es admin
    if (isAdmin) {
      loadDashboardData();
    } else {
      setLoading(false);
    }
  }, [isAdmin]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [resumenData, canchasData] = await Promise.all([
        reportesService.getResumenGeneral(),
        reportesService.getCanchasMasUtilizadas(5)
      ]);
      setResumen(resumenData);
      setTopCanchas(canchasData);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al cargar datos del dashboard');
      console.error('Error loading dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS'
    }).format(amount);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // Landing page para usuarios públicos y clientes
  if (!isAdmin) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
        {/* Hero Section */}
        <section className="relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20"></div>
          <div className="relative max-w-7xl mx-auto px-6 py-24 sm:py-32">
            <div className="text-center">
              <h1 className="text-5xl sm:text-6xl font-bold text-white mb-6">
                Reserva tu Cancha
                <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
                  En Minutos
                </span>
              </h1>
              <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
                Las mejores canchas de fútbol, básquet y pádel. Reserva online de forma rápida y segura.
              </p>
              <div className="flex gap-4 justify-center">
                <button
                  onClick={() => navigate('/canchas-publicas')}
                  className="px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
                >
                  Ver Canchas Disponibles
                </button>
                {user && (
                  <button
                    onClick={() => navigate('/mis-reservas')}
                    className="px-8 py-4 bg-white/10 backdrop-blur-sm hover:bg-white/20 text-white font-semibold rounded-xl border border-white/20 transition-all"
                  >
                    Mis Reservas
                  </button>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 px-6">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-3xl font-bold text-white text-center mb-12">
              ¿Por qué elegirnos?
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/10 hover:border-blue-500/50 transition-all">
                <div className="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center mb-4">
                  <CalendarIcon className="w-6 h-6 text-blue-400" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Reserva Fácil</h3>
                <p className="text-gray-400">
                  Sistema de reservas online intuitivo. Consulta disponibilidad en tiempo real y reserva en segundos.
                </p>
              </div>

              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/10 hover:border-purple-500/50 transition-all">
                <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mb-4">
                  <Squares2X2Icon className="w-6 h-6 text-purple-400" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Mejores Canchas</h3>
                <p className="text-gray-400">
                  Canchas profesionales de fútbol, básquet y pádel con excelente mantenimiento e instalaciones.
                </p>
              </div>

              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/10 hover:border-green-500/50 transition-all">
                <div className="w-12 h-12 bg-green-500/20 rounded-xl flex items-center justify-center mb-4">
                  <CurrencyDollarIcon className="w-6 h-6 text-green-400" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Precios Accesibles</h3>
                <p className="text-gray-400">
                  Tarifas competitivas y transparentes. Servicios adicionales opcionales para mejorar tu experiencia.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Sports Section */}
        <section className="py-20 px-6 bg-black/20">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-3xl font-bold text-white text-center mb-12">
              Nuestros Deportes
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div 
                onClick={() => navigate('/canchas-publicas?deporte=futbol')}
                className="relative group overflow-hidden rounded-2xl cursor-pointer transform hover:scale-105 transition-all duration-300"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-green-600 to-green-800"></div>
                <div className="relative p-8 text-white">
                  <h3 className="text-2xl font-bold mb-2">Fútbol</h3>
                  <p className="text-green-100">Canchas de 5, 7 y 11 jugadores</p>
                </div>
              </div>

              <div 
                onClick={() => navigate('/canchas-publicas?deporte=basquet')}
                className="relative group overflow-hidden rounded-2xl cursor-pointer transform hover:scale-105 transition-all duration-300"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-orange-600 to-orange-800"></div>
                <div className="relative p-8 text-white">
                  <h3 className="text-2xl font-bold mb-2">Básquet</h3>
                  <p className="text-orange-100">Canchas profesionales techadas</p>
                </div>
              </div>

              <div 
                onClick={() => navigate('/canchas-publicas?deporte=padel')}
                className="relative group overflow-hidden rounded-2xl cursor-pointer transform hover:scale-105 transition-all duration-300"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-blue-600 to-blue-800"></div>
                <div className="relative p-8 text-white">
                  <h3 className="text-2xl font-bold mb-2">Pádel</h3>
                  <p className="text-blue-100">Canchas indoor y outdoor</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-6">
          <div className="max-w-4xl mx-auto text-center">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl p-12">
              <h2 className="text-4xl font-bold text-white mb-4">
                ¿Listo para jugar?
              </h2>
              <p className="text-xl text-white/90 mb-8">
                {user 
                  ? 'Encuentra tu cancha ideal y reserva ahora'
                  : 'Crea tu cuenta y comienza a reservar en minutos'
                }
              </p>
              <button
                onClick={() => user ? navigate('/canchas-publicas') : openModal('register')}
                className="px-10 py-4 bg-white hover:bg-gray-100 text-blue-600 font-bold rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
              >
                {user ? 'Ver Canchas' : 'Crear Cuenta Gratis'}
              </button>
            </div>
          </div>
        </section>
      </main>
    );
  }

  // Dashboard para administradores
  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-red-600 dark:text-red-400 mb-4">{error}</p>
          <button
            onClick={loadDashboardData}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <main className="p-6 bg-gray-50 dark:bg-gray-900 min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Panel de Administración
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Bienvenido, {user?.nombre || 'Administrador'}
          </p>
        </div>

        {/* Stats Grid */}
        {resumen && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <StatCard
              title="Total de Canchas"
              value={resumen.total_canchas}
              icon={<Squares2X2Icon className="w-6 h-6" />}
              subtitle="Canchas disponibles"
            />
            <StatCard
              title="Clientes Totales"
              value={resumen.total_clientes}
              icon={<UsersIcon className="w-6 h-6" />}
              subtitle={`${resumen.clientes_activos} activos`}
            />
            <StatCard
              title="Reservas Totales"
              value={resumen.total_reservas}
              icon={<CalendarIcon className="w-6 h-6" />}
              subtitle="Todas las reservas"
            />
            <StatCard
              title="Ingresos Totales"
              value={formatCurrency(resumen.total_ingresos)}
              icon={<CurrencyDollarIcon className="w-6 h-6" />}
              subtitle={`Promedio: ${formatCurrency(resumen.ingreso_promedio_por_reserva)}`}
            />
          </div>
        )}

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div 
            onClick={() => navigate('/turnos')}
            className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-md p-6 text-white hover:shadow-lg transition-shadow cursor-pointer"
          >
            <CalendarIcon className="w-8 h-8 mb-3" />
            <h3 className="text-lg font-semibold mb-2">Gestionar Turnos</h3>
            <p className="text-sm text-blue-100">Administra las reservas y horarios</p>
          </div>

          <div 
            onClick={() => navigate('/pagos')}
            className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow-md p-6 text-white hover:shadow-lg transition-shadow cursor-pointer"
          >
            <CurrencyDollarIcon className="w-8 h-8 mb-3" />
            <h3 className="text-lg font-semibold mb-2">Ver Pagos</h3>
            <p className="text-sm text-green-100">Revisa el estado de pagos</p>
          </div>

          <div 
            onClick={() => navigate('/reportes')}
            className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow-md p-6 text-white hover:shadow-lg transition-shadow cursor-pointer"
          >
            <ChartBarIcon className="w-8 h-8 mb-3" />
            <h3 className="text-lg font-semibold mb-2">Reportes</h3>
            <p className="text-sm text-purple-100">Analiza estadísticas detalladas</p>
          </div>

          <div 
            onClick={() => navigate('/torneos')}
            className="bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-lg shadow-md p-6 text-white hover:shadow-lg transition-shadow cursor-pointer"
          >
            <TrophyIcon className="w-8 h-8 mb-3" />
            <h3 className="text-lg font-semibold mb-2">Torneos</h3>
            <p className="text-sm text-yellow-100">Gestiona torneos y competencias</p>
          </div>

          <div 
            onClick={() => navigate('/clientes')}
            className="bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-lg shadow-md p-6 text-white hover:shadow-lg transition-shadow cursor-pointer"
          >
            <UserGroupIcon className="w-8 h-8 mb-3" />
            <h3 className="text-lg font-semibold mb-2">Clientes</h3>
            <p className="text-sm text-indigo-100">Administra clientes y usuarios</p>
          </div>

          <div 
            onClick={() => navigate('/canchas')}
            className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg shadow-md p-6 text-white hover:shadow-lg transition-shadow cursor-pointer"
          >
            <Squares2X2Icon className="w-8 h-8 mb-3" />
            <h3 className="text-lg font-semibold mb-2">Canchas</h3>
            <p className="text-sm text-orange-100">Gestiona canchas y disponibilidad</p>
          </div>
        </div>

        {/* Top Canchas */}
        {topCanchas.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <div className="flex items-center mb-6">
              <ArrowTrendingUpIcon className="w-6 h-6 text-blue-600 dark:text-blue-400 mr-2" />
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                Canchas Más Utilizadas
              </h2>
            </div>
            <div className="space-y-4">
              {topCanchas.map((cancha, index) => (
                <div
                  key={cancha.id_cancha}
                  className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                >
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-white">
                        {cancha.nombre_cancha}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {cancha.tipo_cancha}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="flex items-center text-sm text-gray-600 dark:text-gray-400 mb-1">
                      <TrophyIcon className="w-4 h-4 mr-1" />
                      {cancha.cantidad_reservas} reservas
                    </div>
                    <p className="font-semibold text-green-600 dark:text-green-400">
                      {formatCurrency(cancha.ingresos_totales)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Footer Info */}
        {resumen && (
          <div className="mt-8 text-center text-sm text-gray-500 dark:text-gray-400">
            <ClockIcon className="w-4 h-4 inline mr-1" />
            Última actualización: {new Date(resumen.fecha_generacion).toLocaleString('es-AR')}
          </div>
        )}
      </div>
    </main>
  );
}
