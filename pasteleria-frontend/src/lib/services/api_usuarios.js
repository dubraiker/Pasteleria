import { get } from 'svelte/store';
import { tokenSesion } from '$lib/stores/authStore.js';
import { API_BASE_URL } from '$lib/config.js';

export async function actualizarUsuarioAPI(idUsuario, datosUsuario, token = null) {
  const jwtToken = token || get(tokenSesion);
  
  const res = await fetch(`${API_BASE_URL}/usuarios/${idUsuario}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${jwtToken}`
    },
    body: JSON.stringify(datosUsuario)
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Error al actualizar usuario');
  return data;
}