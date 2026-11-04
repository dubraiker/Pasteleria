const URL_IOT = '/api/iot';

export async function obtenerAlertasPendientes() {
  const res = await fetch(`${URL_IOT}/alertas/pendientes`);
  if (!res.ok) throw new Error('Error al consultar alertas pendientes');
  return await res.json();
}

export async function atenderAlerta(alertaId, usuarioId) {
  const res = await fetch(`${URL_IOT}/alertas/${alertaId}/atender?id_usuario=${usuarioId}`, {
    method: 'PUT'
  });
  if (!res.ok) throw new Error('Error al procesar la atención de la alerta');
  return await res.json();
}

export async function obtenerLecturasSensor(dispositivoId) {
  const res = await fetch(`${URL_IOT}/dispositivos/${dispositivoId}/lecturas?limite=15`);
  if (!res.ok) throw new Error('Error al obtener lecturas del sensor');
  return await res.json();
}