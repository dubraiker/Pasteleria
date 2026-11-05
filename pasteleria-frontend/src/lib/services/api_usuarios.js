import { API_BASE_URL } from '$lib/config.js';

// src/lib/services/api_usuarios.js
export async function obtenerUsuarios(token) {
  const res = await fetch('/api/usuarios/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!res.ok) {
    throw new Error('Error al obtener la lista de usuarios');
  }

  return await res.json();
}

export async function registrarCliente(datosCliente) {
  const res = await fetch(`${API_BASE_URL}/usuarios/registro`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datosCliente)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Error al registrar cliente');
  }
  return await res.json();
}