import axios from 'axios';
const api_url =  'http://127.0.0.1:8000/api/equipos'

//  SERVICE
const getAllEquipos = async () => {
    const response = await axios.get(`${api_url}/`);
    // normalizar distintos formatos de respuesta (Items, items o array directo)
    const data = response.data?.Items ?? response.data?.items ?? response.data ?? [];
    const list = Array.isArray(data) ? data : [];
    // asegurar que sólo devuelva Equipos cuyo deporte sea básquet (case-insensitive)

    return list;
};

const getEquipoByName = async (name: string) => {
    // intento de pedir al backend por nombre (si el endpoint acepta query params)
    const response = await axios.get(`${api_url}`, { params: { name } });
    const data = response.data?.Items ?? response.data?.items ?? response.data ?? [];
    const list = Array.isArray(data) ? data : [];

        // filtrar por nombre + deporte =  (comparación case-insensitive)
    const nameLower = (name ?? '').toString().toLowerCase();
    return list.filter((item: any) => {
        const itemName = (item?.nombre_equipo ??'').toString().toLowerCase();
        return itemName.includes(nameLower);
    });
}

const getById = async (id: number) => {
        // intento de pedir al backend por nombre (si el endpoint acepta query params)
    try {
            // 1. Petición directa al ID (asumiendo que tu backend es /Equipos/{id})
            // OJO: Si tu api_url ya tiene una barra al final, quítasela aquí o en la variable.
            const response = await axios.get(`${api_url}/${id}`); 

            console.log("📦 Objeto recibido del Back:", response.data);

            // 2. No filtramos nada. Devolvemos el objeto directo.
            // Si tu backend devuelve { nombre: "...", ... } lo devolvemos directo.
            return response.data; 

        } catch (error) {
            console.error("❌ Error obteniendo Equipo por ID:", error);
            return null;
        }
};


const deleteEquipo = async (id: number) => {
    const response = await axios.delete(`${api_url}/${id}`);
    return response.data;
}

const putEquipo = async (id: number, payload: any) => {
    const response = await axios.put(`${api_url}/${id}`, payload);
    return response.data;
}

const creatEquipo = async (payload: any) => {
    const response = await axios.post(`${api_url}/`, payload);
    return response.data;
}


export default {
    // 
    getAllEquipos,
    getEquipoByName,
    deleteEquipo,
    getById,
    actualizarEquipo: putEquipo,
    creatEquipo

};