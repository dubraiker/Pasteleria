import { API_BASE_URL } from '$lib/config.js';

export async function loginAPI(correo, password) {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ correo, password })
  });
  
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Credenciales inválidas o cuenta inactiva');
  return data;
}

export async function registrarCliente(datos) {
  const res = await fetch(`${API_BASE_URL}/usuarios/registro`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  });
  
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Error al registrar la cuenta de cliente');
  return data;
}