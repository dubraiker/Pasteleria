import { get } from 'svelte/store';
import { tokenSesion } from '$lib/stores/authStore.js';

export async function actualizarUsuarioAPI(idUsuario, datosUsuario) {
  const token = get(tokenSesion);
  const res = await fetch(`/api/usuarios/${idUsuario}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(datosUsuario)
  });
  
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Error al actualizar usuario');
  return data;
}