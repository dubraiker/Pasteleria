const URL_AUTH = '/api/auth/login';
const URL_REGISTRO = '/api/usuarios/registro';
import { API_BASE_URL } from '$lib/config.js';

export async function loginAPI(correo, password) {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ correo, password })
  });
  
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Error en las credenciales');
  return data;
}

export async function iniciarSesion(correo, password) {
  const respuesta = await fetch(URL_AUTH, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ correo, password })
  });
  if (!respuesta.ok) throw new Error('Credenciales inválidas o cuenta inactiva');
  return await respuesta.json();
}

export async function registrarCliente(datos) {
  const respuesta = await fetch(URL_REGISTRO, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  });
  if (!respuesta.ok) throw new Error('Error al registrar la cuenta de cliente');
  return await respuesta.json();
}