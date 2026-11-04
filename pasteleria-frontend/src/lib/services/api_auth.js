import { API_BASE_URL } from '$lib/config.js';

export async function loginAPI(correo, password) {
  const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json' 
    },
    body: JSON.stringify({ correo, password })
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Error al iniciar sesión');
  }
  return data;
}

export async function registrarCliente(datos) {
  const payload = {
    nombre: datos.nombre,
    apellido: datos.apellido,
    correo: datos.correo,
    password: datos.password,
    id_rol: 3 
  };

  const res = await fetch(`${API_BASE_URL}/api/auth/registro`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json' 
    },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Error al registrar la cuenta');
  }
  return data;
}