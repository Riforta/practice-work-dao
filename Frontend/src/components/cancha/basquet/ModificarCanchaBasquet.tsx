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
};

export default function ModificarCanchaBasquet() {
  const { register, handleSubmit, formState: { errors }, setValue, reset } = useForm<FormData>();
  const params = useParams();
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState("");

  const id = params.id || params.Id || params.Id_Cancha;

  useEffect(() => {
    if (!id) return;
    const fetchCancha = async () => {
      try {
        const data: any = await service.getByIdBasquet(Number(id));
        if (!data) return;
        
        // Asignamos valores
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
    try {
      const payload = {
        nombre: form.nombre,
        tipo_deporte: form.tipo_deporte,
        descripcion: form.descripcion,
        activa: form.activa,
      };
      
      // 1. Esperamos a que el backend responda
      await service.actualizarCancha(Number(id), payload);
      
      // 2. SI todo salió bien, entonces navegamos
      // Cambié la ruta a '/canchas/basquet' para coincidir con tu intención original
      navigate("/canchas/basquet"); 
      
    } catch (err) {
      console.error(err);
      setErrorMessage("Error al actualizar la cancha. Verifique los datos.");
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
        {errorMessage && <div className="text-red-400 mb-4">{errorMessage}</div>}

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
            <option value="" className="bg-gray-700">-- Seleccione --</option>
          <option value="futbol" className="bg-gray-700">Futbol</option>
          <option value="padel" className="bg-gray-700">Padel</option>
          <option value="basquet" className="bg-gray-700">Basquet</option>
        </select>
        {errors.tipo_deporte && <p className="text-red-400 text-sm mb-2">{errors.tipo_deporte.message}</p>}

        <label className="block mb-2 text-sm">Descripción</label>
        <textarea
          {...register("descripcion")}
          className="w-full mb-3 px-3 py-2 rounded bg-white/5 focus:outline-none focus:ring-2 focus:ring-white/30"
          rows={3}
        />

        <label className="flex items-center gap-2 mb-4">
          <input
            type="checkbox"
            {...register("activa")}
            className="w-4 h-4 text-blue-500 bg-white/5 rounded focus:ring-2 focus:ring-white/30"
          />
          <span className="text-sm">Activa</span>
        </label>

        <div className="flex justify-center gap-3 mt-4">
          
          {/* CORRECCIÓN: Quitamos el Link que envolvía al botón */}
          <button
            type="submit"
            className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded text-white"
          >
            Actualizar
          </button>
          
          <button
            type="button"
            onClick={() => { reset(); }}
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
