import {
  InboxIcon,
  UserCircleIcon,
  BanknotesIcon,
  HomeIcon,
  CalendarIcon,
  UsersIcon,
} from '@heroicons/react/24/outline';
import { useAuth } from '../../contexts/AuthContext';

// --- El componente se llama 'Sidebar' y es la exportación por defecto ---

export default function Sidebar() {
  const { user } = useAuth();
  
  // Determinar rol del usuario
  const isAdmin = user?.id_rol === 1;
  const isCliente = user?.id_rol === 2;

  // Navegación pública (usuarios no autenticados)
  const navigationPublic = [
    { name: 'Inicio', href: '/', icon: HomeIcon, current: false },
    { name: 'Canchas Disponibles', href: '/canchas-publicas', icon: InboxIcon, current: false },
  ];

  // Navegación cliente (usuarios autenticados como cliente)
  const navigationCliente = [
    { name: 'Inicio', href: '/', icon: HomeIcon, current: false },
    { name: 'Canchas Disponibles', href: '/canchas-publicas', icon: InboxIcon, current: false },
    { name: 'Mis Reservas', href: '/mis-reservas', icon: CalendarIcon, current: false },
  ];

  // Navegación admin (usuarios con rol administrador)
  const navigationAdmin = [
    { name: 'Inicio', href: '/', icon: HomeIcon, current: false },
    { name: 'Canchas', href: '/canchas', icon: InboxIcon, current: false },
    { name: 'Clientes', href: '/clientes', icon: UsersIcon, current: false },
    { name: 'Equipos', href: '/equipos', icon: UserCircleIcon, current: false },
    { name: 'Pagos', href: '/pagos', icon: BanknotesIcon, current: false },
    { name: 'Torneos', href: '/torneos', icon: UserCircleIcon, current: false },
    { name: 'Servicios', href: '/servicios', icon: UserCircleIcon, current: false },
    { name: 'Turnos', href: '/turnos', icon: UserCircleIcon, current: false },
  ];

  // Seleccionar navegación según rol
  let navigation = navigationPublic;
  if (isAdmin) {
    navigation = navigationAdmin;
  } else if (isCliente) {
    navigation = navigationCliente;
  }



  // Función de utilidad para clases condicionales
  function classNames(...classes: (string | boolean | null | undefined)[]) {
    return classes.filter(Boolean).join(' ');
  }

  return (
    <div className="flex h-full w-72 flex-col bg-gray-900 text-white">
      {/* Contenido principal del Sidebar */}
      <div className="flex flex-1 flex-col overflow-y-auto">
        <nav className="flex-1 space-y-1 px-4 py-4">
          {navigation.map((item) => (
            <div key={item.name}>
              <a
                href={item.href}
                className={classNames(
                  item.current
                    ? 'bg-gray-800 text-white'
                    : 'text-gray-400 hover:bg-gray-800 hover:text-white',
                  'group flex items-center gap-x-3 rounded-md px-3 py-2 text-sm font-medium transition-colors duration-150',
                )}
              >
                <item.icon
                  className={classNames(
                    item.current
                      ? 'text-white'
                      : 'text-gray-500 group-hover:text-white',
                    'size-6 shrink-0 transition-colors duration-150',
                  )}
                  aria-hidden="true"
                />
                <span className="flex-1">{item.name}</span>
              </a>
            </div>
          ))}
        </nav>
      </div>
    </div>
  );
}
