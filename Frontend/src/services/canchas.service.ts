import axios from 'axios';
const api_url =  'http://127.0.0.1:8000/canchas'


const getAllCanchasBasquet = async () => {
    const response = await axios.get(`${api_url}/`);
    // normalizar distintos formatos de respuesta (Items, items o array directo)
    const data = response.data?.Items ?? response.data?.items ?? response.data ?? [];
    const list = Array.isArray(data) ? data : [];
    // asegurar que sólo devuelva canchas cuyo deporte sea básquet (case-insensitive)
    const isBasket = (item: any) => {
        const val = (item?.deporte ?? item?.Deporte ?? item?.tipo ?? item?.tipo_deporte ?? item?.Tipo_deporte ?? '').toString().toLowerCase();
        return val === 'basquet' || val === 'básquet' || val === 'basket' || val === 'basketball';
    };
    return list.filter(isBasket);
};

const getCanchaBasquetByName = async (name: string) => {
    // intento de pedir al backend por nombre (si el endpoint acepta query params)
    const response = await axios.get(`${api_url}`, { params: { name } });
    const data = response.data?.Items ?? response.data?.items ?? response.data ?? [];
    const list = Array.isArray(data) ? data : [];

    const isBasket = (item: any) => {
        const val = (item?.deporte ?? item?.Deporte ?? item?.tipo ?? item?.tipo_deporte ?? item?.Tipo_deporte ?? '').toString().toLowerCase();
        return val === 'basquet' || val === 'básquet' || val === 'basket' || val === 'basketball';
    };

        // filtrar por nombre + deporte = basquet (comparación case-insensitive)
    const nameLower = (name ?? '').toString().toLowerCase();
    return list.filter((item: any) => {
        const itemName = (item?.nombre ?? item?.Nombre ?? item?.nombre_del_estadio ?? item?.Nombre_del_Estadio ?? '').toString().toLowerCase();
        return itemName.includes(nameLower) && isBasket(item);
    });
}

const getByIdBasquet = async (id: number) => {
        // intento de pedir al backend por nombre (si el endpoint acepta query params)
    try {
            // 1. Petición directa al ID (asumiendo que tu backend es /canchas/{id})
            // OJO: Si tu api_url ya tiene una barra al final, quítasela aquí o en la variable.
            const response = await axios.get(`${api_url}/${id}`); 

            console.log("📦 Objeto recibido del Back:", response.data);

            // 2. No filtramos nada. Devolvemos el objeto directo.
            // Si tu backend devuelve { nombre: "...", ... } lo devolvemos directo.
            return response.data; 

        } catch (error) {
            console.error("❌ Error obteniendo cancha por ID:", error);
            return null;
        }
};


const deleteCanchaBasquet = async (id: number) => {
    const response = await axios.delete(`${api_url}/${id}`);
    return response.data;
}

const putCanchaBasquet = async (id: number, payload: any) => {
    const response = await axios.put(`${api_url}/${id}`, payload);
    return response.data;
}

export default {
    getAllCanchasBasquet,
    getCanchaBasquetByName,
    deleteCanchaBasquet,
    getByIdBasquet,
    actualizarCancha: putCanchaBasquet
};