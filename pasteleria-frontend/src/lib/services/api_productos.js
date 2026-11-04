import { API_BASE_URL } from '$lib/config.js';

export async function obtenerProductos() {
  const res = await fetch(`${API_BASE_URL}/productos/`);
  if (!res.ok) throw new Error('Error al obtener la lista de productos');
  return await res.json();
}

export async function crearProducto(producto, token) {
  const res = await fetch(`${API_BASE_URL}/productos/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(producto)
  });
  if (!res.ok) throw new Error('Error al registrar el producto');
  return await res.json();
}

export async function desactivarProducto(id, token) {
  const res = await fetch(`${API_BASE_URL}/productos/${id}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Error al desactivar el producto');
  return await res.json();
}