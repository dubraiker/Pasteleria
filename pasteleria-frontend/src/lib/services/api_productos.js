const URL_PRODUCTOS = '/api/productos/';

export async function obtenerProductos() {
  const res = await fetch(URL_PRODUCTOS);
  if (!res.ok) throw new Error('Error al obtener la lista de productos');
  return await res.json();
}

export async function crearProducto(producto, token) {
  const res = await fetch(URL_PRODUCTOS, {
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
  const res = await fetch(`${URL_PRODUCTOS}${id}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Error al desactivar el producto');
  return await res.json();
}