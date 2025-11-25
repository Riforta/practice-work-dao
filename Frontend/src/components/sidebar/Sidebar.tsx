import React from 'react';
import logo from './Logo.png';
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/react';
import {
  RectangleStackIcon,
  ShoppingCartIcon,
  ChevronDownIcon,
  InboxIcon,
  UserCircleIcon,
  ArrowRightStartOnRectangleIcon,
  BanknotesIcon,
} from '@heroicons/react/24/outline';

// --- El componente se llama 'Sidebar' y es la exportación por defecto ---

export default function Sidebar() {
  // const currentItem = 'Reservas'; // ⬆️ ELIMINÉ ESTA LÍNEA

  const navigation = [
    { name: 'Reservas', href: '#', icon: RectangleStackIcon}, // 'current: true' ahora controla el estado activo
    {
      name: 'Clientes',
      icon: ShoppingCartIcon,
      current: false,
      children: [
        { name: 'Orders', href: '#' },
        { name: 'Products', href: '#' },
      ],
    },
    { name: 'Canchas', href: '/canchas', icon: InboxIcon, current: false, count: '14' },
    { name: 'Equipos', href: '/equipos', icon: UserCircleIcon, current: false },
    { name: 'Pagos', href: '/pagos', icon: BanknotesIcon, current: false },
    { name: 'Torneos', href: '/torneos', icon: UserCircleIcon, current: false },
    { name: 'Servicios', href: '/servicios', icon: UserCircleIcon, current: false },
    { name: 'Turnos', href: '/turnos', icon: UserCircleIcon, current: false },

  ];



  // Función de utilidad para clases condicionales
  function classNames(...classes: (string | boolean | null | undefined)[]) {
    return classes.filter(Boolean).join(' ');
  }

  return (
    <div className="flex h-full min-h-screen w-72 flex-col bg-gray-900 text-white">
      {/* Encabezado del Sidebar (Logo/Título) */}

      {/* Contenido principal del Sidebar */}
      <div className="flex flex-1 flex-col overflow-y-auto">
        <nav className="flex-1 space-y-1 px-4 py-4">
          {navigation.map((item) =>
            !item.children ? (
              // --- Elemento de link normal ---
              <div key={item.name}>
                <a
                  href={item.href}
                  className={classNames(
                    item.current // ⬆️ MODIFICADO: Ahora usa 'item.current'
                      ? 'bg-gray-800 text-white' // Estado activo
                      : 'text-gray-400 hover:bg-gray-800 hover:text-white', // Estado normal
                    'group flex items-center gap-x-3 rounded-md px-3 py-2 text-sm font-medium transition-colors duration-150',
                  )}
                >
                  <item.icon
                    className={classNames(
                      item.current // ⬆️ MODIFICADO: Ahora usa 'item.current'
                        ? 'text-white'
                        : 'text-gray-500 group-hover:text-white',
                      'size-6 shrink-0 transition-colors duration-150',
                    )}
                    aria-hidden="true"
                  />
                  <span className="flex-1">{item.name}</span>
                  {item.count ? (
                    <span className="ml-auto whitespace-nowrap rounded-full bg-indigo-500 px-2.5 py-0.5 text-xs font-medium text-white">
                      {item.count}
                    </span>
                  ) : null}
                </a>
              </div>
            ) : (
              // --- Elemento de Disclosure (Submenú) ---
              <Disclosure as="div" key={item.name} className="space-y-1" defaultOpen={true}>
                <DisclosureButton
                  className={classNames(
                    item.current
                      ? 'bg-gray-800 text-white'
                      : 'text-gray-400 hover:bg-gray-800 hover:text-white',
                    'group flex w-full items-center gap-x-3 rounded-md px-3 py-2 text-left text-sm font-medium transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                  )}
                >
                  <item.icon
                    className="size-6 shrink-0 text-gray-500 group-hover:text-white"
                    aria-hidden="true"
                  />
                  <span className="flex-1">{item.name}</span>
                  <ChevronDownIcon
                    className="size-5 shrink-0 text-gray-500 transition-transform duration-150 ease-in-out group-data-open:rotate-180"
                    aria-hidden="true"
                  />
                </DisclosureButton>
                <DisclosurePanel className="space-y-1 pl-9">
                  {item.children.map((subItem) => (
                    <a
                      key={subItem.name}
                      href={subItem.href}
                      className="group flex items-center gap-x-3 rounded-md py-2 pl-3 pr-2 text-sm font-medium text-gray-400 hover:bg-gray-800 hover:text-white"
                    >
                      {subItem.name}
                    </a>
                  ))}
                </DisclosurePanel>
              </Disclosure>
            )
          )}
        </nav>
      </div>
    </div>
  );
}