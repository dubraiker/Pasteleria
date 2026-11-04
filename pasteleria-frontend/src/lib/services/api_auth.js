const URL_AUTH = '/api/auth/login';
const URL_REGISTRO = '/api/usuarios/registro';

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