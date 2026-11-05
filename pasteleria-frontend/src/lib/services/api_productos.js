import { API_BASE_URL } from '$lib/config.js';



export async function obtenerProductos() {
  const res = await fetch('/api/productos/');
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || 'Error al obtener la lista de productos');
  }
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
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Error al registrar producto');
  }
  return await res.json();
}

export async function desactivarProducto(id, token) {
  const res = await fetch(`${API_BASE_URL}/productos/${id}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Error al eliminar producto');
  return await res.json();
}