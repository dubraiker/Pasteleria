import { API_BASE_URL } from '$lib/config.js';

export async function obtenerAlertasPendientes() {
  const res = await fetch(`${API_BASE_URL}/iot/alertas/pendientes`);
  if (!res.ok) throw new Error('Error al consultar alertas pendientes');
  return await res.json();
}

export async function atenderAlerta(alertaId, usuarioId) {
  const res = await fetch(`${API_BASE_URL}/iot/alertas/${alertaId}/atender?id_usuario=${usuarioId}`, {
    method: 'PUT'
  });
  if (!res.ok) throw new Error('Error al procesar la atención de la alerta');
  return await res.json();
}

export async function obtenerLecturasSensor(dispositivoId) {
  const res = await fetch(`${API_BASE_URL}/iot/dispositivos/${dispositivoId}/lecturas?limite=15`);
  if (!res.ok) throw new Error('Error al obtener lecturas del sensor');
  return await res.json();
}