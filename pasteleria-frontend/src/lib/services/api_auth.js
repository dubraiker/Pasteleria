// src/lib/services/api_auth.js
export async function loginUsuario(correo, password) {
  const respuesta = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ correo, password })
  });

  if (!respuesta.ok) {
    const errorData = await respuesta.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Credenciales incorrectas');
  }

  return await respuesta.json();
}