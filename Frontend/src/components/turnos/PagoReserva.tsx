import { useState, useMemo } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import turnosApi, { type Turno, type CanchaRef } from '../../services/turnos.service';

type NavState = {
  turno: Turno;
  cancha: CanchaRef;
};

const currency = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 0 });

const luhnValido = (value: string) => {
  const digits = value.replace(/\D/g, '');
  let sum = 0;
  let shouldDouble = false;
  for (let i = digits.length - 1; i >= 0; i -= 1) {
    let digit = parseInt(digits.charAt(i), 10);
    if (shouldDouble) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }
    sum += digit;
    shouldDouble = !shouldDouble;
  }
  return sum % 10 === 0;
};

export default function PagoReserva() {
  const navigate = useNavigate();
  const location = useLocation();
  const state = location.state as NavState | undefined;

  const { user } = useAuth();
  const clienteSesionId = useMemo(() => {
    if (!user) return null;
    return user.id_cliente ?? user.cliente_id ?? null;
  }, [user]);
  const [pago, setPago] = useState({ numero: '', nombre: '', vencimiento: '', cvv: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!state?.turno || !state?.cancha) {
    return (
      <div className="min-h-screen bg-slate-950 text-white px-4 py-10 flex items-center justify-center">
        <div className="max-w-md w-full space-y-3 text-center">
          <p className="text-sm uppercase tracking-widest text-emerald-200">Pago</p>
          <h1 className="text-2xl font-bold">No se encontró la selección</h1>
          <p className="text-emerald-100/80 text-sm">Vuelve a seleccionar un turno disponible para proceder con el pago.</p>
          <button
            onClick={() => navigate('/reservas')}
            className="mt-3 rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400"
          >
            Volver a reservas
          </button>
        </div>
      </div>
    );
  }

  const { turno, cancha } = state;

  const handlePagar = async () => {
    setError('');
    if (!clienteSesionId) {
      setError('Inicia sesión para continuar.');
      return;
    }
    if (!pago.nombre.trim()) {
      setError('Ingresa el nombre del titular.');
      return;
    }
    if (!luhnValido(pago.numero)) {
      setError('Número de tarjeta inválido.');
      return;
    }
    if (!/^(0[1-9]|1[0-2])\/\d{2}$/.test(pago.vencimiento)) {
      setError('Vencimiento inválido. Usa MM/AA.');
      return;
    }
    const [mm, aa] = pago.vencimiento.split('/').map(Number);
    const expDate = new Date(2000 + aa, mm - 1, 1);
    const now = new Date();
    if (expDate < new Date(now.getFullYear(), now.getMonth(), 1)) {
      setError('La tarjeta está vencida.');
      return;
    }
    if (!/^\d{3,4}$/.test(pago.cvv)) {
      setError('CVV inválido.');
      return;
    }

    setLoading(true);
    try {
      await turnosApi.reservarSimple(turno.id!, clienteSesionId);
      navigate('/reservas');
    } catch (err) {
      console.error(err);
      setError('No se pudo completar el pago/reserva.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-3xl mx-auto space-y-6">
        <header className="space-y-2">
          <p className="text-sm uppercase tracking-widest text-emerald-200">Pago</p>
          <h1 className="text-3xl font-bold">Confirmar y pagar</h1>
          {error && <p className="text-red-300 text-sm">{error}</p>}
        </header>

        <div className="rounded-2xl bg-white/10 border border-white/10 p-5 shadow-xl backdrop-blur-md space-y-4">
          <div className="rounded-lg bg-white/5 p-3 text-sm text-emerald-100/90">
            <p className="font-semibold">{cancha.nombre}</p>
            <p className="text-emerald-200">{cancha.tipo_deporte ?? 'Deporte'}</p>
            <p>
              {new Date(turno.fecha_hora_inicio).toLocaleString('es-AR', { dateStyle: 'medium', timeStyle: 'short' })} -{' '}
              {new Date(turno.fecha_hora_fin).toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })}
            </p>
            <p className="font-semibold">{currency.format(turno.precio_final)}</p>
          </div>

          <div className="grid gap-3">
            <label className="text-sm">
              Nombre en la tarjeta
              <input
                value={pago.nombre}
                onChange={(e) => setPago({ ...pago, nombre: e.target.value })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
              />
            </label>
            <label className="text-sm">
              Número de tarjeta
              <input
                value={pago.numero}
                onChange={(e) => setPago({ ...pago, numero: e.target.value })}
                placeholder="#### #### #### ####"
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
              />
            </label>
            <div className="grid grid-cols-2 gap-3">
              <label className="text-sm">
                Vencimiento (MM/AA)
                <input
                  value={pago.vencimiento}
                  onChange={(e) => setPago({ ...pago, vencimiento: e.target.value })}
                  placeholder="08/27"
                  className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
                />
              </label>
              <label className="text-sm">
                CVV
                <input
                  value={pago.cvv}
                  onChange={(e) => setPago({ ...pago, cvv: e.target.value })}
                  placeholder="***"
                  className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
                />
              </label>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => void handlePagar()}
                className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-60"
                disabled={loading}
              >
                {loading ? 'Procesando...' : 'Pagar y reservar'}
              </button>
              <button
                onClick={() => navigate('/reservas')}
                className="rounded-lg border border-white/20 px-4 py-2 text-sm font-semibold text-emerald-100 hover:border-emerald-400"
              >
                Volver sin pagar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
