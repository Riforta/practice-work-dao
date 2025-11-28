import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import clientesService, { type Cliente } from '../../services/clientes.service';

type FormValues = Omit<Cliente, 'id'>;

export default function RegistrarCliente() {
	const navigate = useNavigate();
	const {
		register,
		handleSubmit,
		formState: { errors, isSubmitting },
	} = useForm<FormValues>();

	const [error, setError] = useState('');
	const [success, setSuccess] = useState('');

	const onSubmit = async (values: FormValues) => {
		setError('');
		setSuccess('');
		try {
			await clientesService.create(values);
			setSuccess('Cliente registrado correctamente. Redirigiendo...');
			setTimeout(() => navigate('/clientes'), 800);
		} catch (err) {
			console.error(err);
			setError('No se pudo registrar el cliente. Revisa los datos e intenta nuevamente.');
		}
	};

	return (
		<div className="min-h-screen bg-slate-950 text-white px-4 py-10">
			<div className="max-w-3xl mx-auto space-y-6">
				<header className="space-y-2">
					<p className="text-sm uppercase tracking-widest text-emerald-200">Clientes</p>
					<h1 className="text-3xl font-bold">Registrar nuevo cliente</h1>
					<p className="text-sm text-emerald-100/70">
						Registra clientes que realizan reservas telefónicas o por otros medios
					</p>
					{error && <p className="text-red-300 text-sm">{error}</p>}
					{success && <p className="text-emerald-200 text-sm">{success}</p>}
				</header>

				<form
					onSubmit={handleSubmit(onSubmit)}
					className="space-y-6 rounded-2xl bg-white/5 p-6 shadow-2xl border border-white/10"
				>
					<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
						<label className="text-sm">
							Nombre <span className="text-red-400">*</span>
							<input
								type="text"
								{...register('nombre', {
									required: 'El nombre es obligatorio',
									minLength: { value: 2, message: 'Mínimo 2 caracteres' },
								})}
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
								placeholder="Ej: Juan"
							/>
							{errors.nombre && (
								<span className="text-xs text-red-300">{errors.nombre.message}</span>
							)}
						</label>

					<label className="text-sm">
						Apellido <span className="text-red-400">*</span>
						<input
							type="text"
							{...register('apellido', {
								required: 'El apellido es obligatorio',
								minLength: { value: 2, message: 'Mínimo 2 caracteres' },
							})}
							className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
							placeholder="Ej: Pérez"
						/>
						{errors.apellido && (
							<span className="text-xs text-red-300">{errors.apellido.message}</span>
						)}
					</label>					<label className="text-sm">
						DNI <span className="text-red-400">*</span>
						<input
							type="text"
							{...register('dni', {
								required: 'El DNI es obligatorio',
								pattern: {
									value: /^[0-9]{7,8}$/,
									message: 'DNI inválido (7-8 dígitos)',
								},
							})}
							className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
							placeholder="Ej: 12345678"
							maxLength={8}
						/>
						{errors.dni && <span className="text-xs text-red-300">{errors.dni.message}</span>}
					</label>					<label className="text-sm">
						Teléfono <span className="text-red-400">*</span>
						<input
							type="tel"
							{...register('telefono', {
								required: 'El teléfono es obligatorio',
								pattern: {
									value: /^[0-9\s\-\+\(\)]{7,20}$/,
									message: 'Teléfono inválido',
								},
							})}
							className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
							placeholder="Ej: 351-1234567"
						/>
						{errors.telefono && (
							<span className="text-xs text-red-300">{errors.telefono.message}</span>
						)}
					</label>						<label className="text-sm md:col-span-2">
							Email
							<input
								type="email"
								{...register('email', {
									pattern: {
										value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
										message: 'Email inválido',
									},
								})}
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
								placeholder="Ej: cliente@email.com"
							/>
							{errors.email && (
								<span className="text-xs text-red-300">{errors.email.message}</span>
							)}
						</label>
					</div>

					<div className="rounded-xl border border-blue-500/30 bg-blue-500/10 p-4">
						<p className="text-xs text-blue-200">
							<span className="font-semibold">Nota:</span> Los campos marcados con{' '}
							<span className="text-red-400">*</span> son obligatorios. Este cliente no
							tendrá acceso al sistema, es solo para registro de reservas telefónicas.
						</p>
					</div>

					<div className="flex flex-wrap gap-3">
						<button
							type="submit"
							disabled={isSubmitting}
							className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-60"
						>
							{isSubmitting ? 'Registrando...' : 'Registrar cliente'}
						</button>
						<button
							type="button"
							onClick={() => navigate('/clientes')}
							className="rounded-lg border border-white/20 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
						>
							Cancelar
						</button>
					</div>
				</form>
			</div>
		</div>
	);
}
