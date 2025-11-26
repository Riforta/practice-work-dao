import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate, useParams } from "react-router-dom";
import service from "../../../services/canchas.service";
import backgroundImage from "./imagenes/curry_hd_si.jpg";

type FormData = {
  nombre: string;
  tipo_deporte: string;
  descripcion: string;
  activa: boolean;
  precio_hora: number;
};

export default function ModificarCanchaBasquet() {
  const { register, handleSubmit, formState: { errors }, setValue, reset } = useForm<FormData>();
  const params = useParams();
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState("");

  const id = params.id || params.Id || params.Id_Cancha;

  // Carga inicial de datos
  useEffect(() => {
    if (!id) return;
    const fetchCancha = async () => {
      try {
        const data: any = await service.getByIdBasquet(Number(id));
        if (!data) return;
        
        setValue("nombre", data.nombre ?? data.Nombre ?? "");
        setValue("tipo_deporte", (data.tipo_deporte ?? data.deporte ?? "").toString().toLowerCase());
        setValue("descripcion", data.descripcion ?? "");
        setValue("activa", Boolean(data.activa));
      } catch (err) {
        console.error(err);
        setErrorMessage("No se pudo cargar la cancha.");
      }
    };
    fetchCancha();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const onSubmit = async (form: FormData) => {
    // Limpiamos errores previos
    setErrorMessage("");

    try {
      // --- PASO 1: VERIFICACIÓN DE NOMBRE DUPLICADO ---
      
      // Buscamos si ya existe alguien con ese nombre
      // (Asumiendo que tienes este método en tu servicio, lo vimos antes)
      const canchasConEseNombre = await service.getCanchaBasquetByName(form.nombre);
      
      // Revisamos si encontramos alguna cancha QUE NO SEA la actual
      // (Comparamos IDs: si el ID es distinto pero el nombre es igual, es un duplicado)
      const existeDuplicado = canchasConEseNombre.some((c: any) => 
        // Asegúrate de comparar usando el nombre exacto y excluyendo el ID actual
        c.nombre.toLowerCase() === form.nombre.toLowerCase() && 
        (c.id || c.Id) !== Number(id)
      );

      if (existeDuplicado) {
        setErrorMessage("⚠️ Ya existe otra cancha con ese nombre. Por favor elija uno distinto.");
        return; // <--- AQUÍ DETENEMOS LA EJECUCIÓN
      }

      // --- PASO 2: ACTUALIZACIÓN ---

      const payload = {
        nombre: form.nombre,
        tipo_deporte: form.tipo_deporte,
        descripcion: form.descripcion,
        activa: form.activa,
      };
      
      await service.actualizarCancha(Number(id), payload);
      
      // --- PASO 3: REDIRECCIÓN ---
      // Si llegamos acá es que no hubo error en el await anterior
      navigate("/canchas/basquet"); 
      
    } catch (err) {
      console.error(err);
      setErrorMessage("Error al actualizar la cancha. Verifique los datos o la conexión.");
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white/10 backdrop-blur-md text-white rounded-lg p-6 w-full max-w-lg shadow-lg"
      >
        <h3 className="text-2xl mb-4">Modificar Cancha</h3>
        
        {/* Mensaje de error destacado */}
        {errorMessage && (
            <div className="bg-red-500/20 border border-red-500 text-red-100 p-3 rounded mb-4 text-sm text-center">
                {errorMessage}
            </div>
        )}

        <label className="block mb-2 text-sm">Nombre</label>
        <input
          {...register("nombre", { required: "El nombre es requerido" })}
          className="w-full mb-3 px-3 py-2 rounded bg-white/5 focus:outline-none focus:ring-2 focus:ring-white/30"
        />
        {errors.nombre && <p className="text-red-400 text-sm mb-2">{errors.nombre.message}</p>}

        <label className="block mb-2 text-sm">Deporte</label>
        <select
          {...register("tipo_deporte", { required: "Seleccione un deporte" })}
          className="w-full mb-3 px-3 py-2 rounded bg-white/5 focus:outline-none focus:ring-2 focus:ring-white/30"
        >
        <option value="basquet" className="bg-gray-700">Basquet</option>
        </select>
        {errors.tipo_deporte && <p className="text-red-400 text-sm mb-2">{errors.tipo_deporte.message}</p>}

        <label className="block mb-2 text-sm">Descripción</label>
        <textarea
          {...register("descripcion")}
          className="w-full mb-3 px-3 py-2 rounded bg-white/5 focus:outline-none focus:ring-2 focus:ring-white/30"
          rows={3}
        />

        <label className="block mb-2 text-sm">Precio x Hora</label>
        <input
          type="number"
          min={10}
          step={1}
          {...register("precio_hora", {
            required: "El precio es requerido",
            valueAsNumber: true,
            min: { value: 10, message: "El precio debe ser mayor o igual a 10" },
          })}
          className="w-full mb-3 px-3 py-2 rounded bg-white/5 focus:outline-none focus:ring-2 focus:ring-white/30"
        />
        {errors.precio_hora && <p className="text-red-400 text-sm mb-2">{errors.precio_hora.message}</p>}

        <label className="flex items-center gap-2 mb-4">
          <input
            type="checkbox"
            {...register("activa")}
            className="w-4 h-4 text-blue-500 bg-white/5 rounded focus:ring-2 focus:ring-white/30"
          />
          <span className="text-sm">Activa</span>
        </label>

        <div className="flex justify-center gap-3 mt-4">
          <button
            type="submit"
            className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded text-white"
          >
            Actualizar
          </button>
          
          <button
            type="button"
            onClick={() => { reset(); setErrorMessage(""); }}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded text-white"
          >
            Limpiar
          </button>
          
          <Link to="/canchas/basquet" className="px-4 py-2 bg-black/60 hover:bg-black/80 rounded text-white flex items-center">
            Volver
          </Link>
        </div>
      </form>
    </div>
  );
}
