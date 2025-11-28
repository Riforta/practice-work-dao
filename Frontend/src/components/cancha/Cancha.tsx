import { useNavigate } from 'react-router-dom';
import { 
  Square3Stack3DIcon,
  PlusCircleIcon,
  MagnifyingGlassIcon 
} from '@heroicons/react/24/outline';

export default function Cancha() {
  const navigate = useNavigate();

  const deportes = [
    {
      nombre: 'Fútbol',
      path: '/canchas/futbol',
      descripcion: 'Canchas de fútbol 5, 7 y 11',
      color: 'from-green-600 to-green-800',
      icon: '⚽'
    },
    {
      nombre: 'Básquet',
      path: '/canchas/basquet',
      descripcion: 'Canchas de básquet profesionales',
      color: 'from-orange-600 to-orange-800',
      icon: '🏀'
    },
    {
      nombre: 'Pádel',
      path: '/canchas/padel',
      descripcion: 'Canchas de pádel indoor y outdoor',
      color: 'from-blue-600 to-blue-800',
      icon: '🎾'
    }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-widest text-emerald-200">Canchas</p>
            <h1 className="text-3xl font-bold">Gestión de Canchas</h1>
            <p className="text-sm text-emerald-100/70 mt-1">
              Selecciona un tipo de deporte para administrar sus canchas
            </p>
          </div>
          <button
            onClick={() => navigate('/')}
            className="min-w-[10rem] rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20"
          >
            Volver
          </button>
        </header>

        {/* Grid de deportes */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {deportes.map((deporte) => (
            <div
              key={deporte.path}
              onClick={() => navigate(deporte.path)}
              className="group rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 transition-all cursor-pointer overflow-hidden"
            >
              {/* Gradient header */}
              <div className={`bg-gradient-to-br ${deporte.color} p-8 relative overflow-hidden`}>
                <div className="absolute inset-0 bg-black/20"></div>
                <div className="relative z-10 text-center">
                  <div className="text-6xl mb-4">{deporte.icon}</div>
                  <h3 className="text-2xl font-bold text-white">{deporte.nombre}</h3>
                </div>
              </div>

              {/* Content */}
              <div className="p-6 space-y-4">
                <p className="text-sm text-emerald-100/70">{deporte.descripcion}</p>
                
                <div className="space-y-2 pt-4 border-t border-white/10">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(deporte.path);
                    }}
                    className="w-full flex items-center justify-center gap-2 rounded-lg bg-emerald-500/20 px-4 py-2.5 text-sm font-semibold text-emerald-200 hover:bg-emerald-500/30 transition-colors"
                  >
                    <MagnifyingGlassIcon className="w-5 h-5" />
                    Consultar Canchas
                  </button>
                  
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`${deporte.path}/RegistrarCancha`);
                    }}
                    className="w-full flex items-center justify-center gap-2 rounded-lg bg-white/5 px-4 py-2.5 text-sm font-semibold text-emerald-100 hover:bg-white/10 transition-colors"
                  >
                    <PlusCircleIcon className="w-5 h-5" />
                    Registrar Nueva
                  </button>
                </div>
              </div>
            </div>
          ))}
        </section>

        {/* Info adicional */}
        <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
          <div className="flex items-start gap-3">
            <Square3Stack3DIcon className="w-5 h-5 text-emerald-200 flex-shrink-0 mt-0.5" />
            <div className="text-sm text-emerald-200">
              <p className="font-semibold mb-1">Gestión de Canchas</p>
              <p className="text-emerald-100/70">
                Desde aquí puedes administrar todas las canchas disponibles. 
                Selecciona el tipo de deporte para ver, editar o crear nuevas canchas.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
