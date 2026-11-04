<script>
  import { onMount } from 'svelte';
  import { obtenerAlertasPendientes, obtenerLecturasSensor } from '$lib/services/api_iot.js';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import MetricCard from '$lib/components/MetricCard.svelte';
  import DataTable from '$lib/components/DataTable.svelte';

  let alertas = [];
  let lecturas = [];
  let ultimaTemp = '--';
  let ultimaHum = '--';

  const columnasAlertas = [
    { key: 'dispositivo_nombre', label: 'Ubicación Sensor' },
    { key: 'tipo_alerta_nombre', label: 'Evento' },
    { key: 'nivel_riesgo', label: 'Riesgo' }
  ];

  async function actualizarPanelAdmin() {
    try {
      alertas = await obtenerAlertasPendientes();
      const datosLecturas = await obtenerLecturasSensor(1); // Dispositivo 1 (Hornos)
      if (datosLecturas.length > 0) {
        ultimaTemp = `${datosLecturas[0].temperatura} °C`;
        ultimaHum = `${datosLecturas[0].humedad} %`;
      }
    } catch (e) {
      console.error(e);
    }
  }

  onMount(() => {
    actualizarPanelAdmin();
    const timer = setInterval(actualizarPanelAdmin, 5000);
    return () => clearInterval(timer);
  });
</script>

<Header 
  titulo="Panel General de Monitoreo IoT (Admin)" 
  subtitulo="Métricas ambientales y supervisión global del estado del establecimiento" 
/>

<div class="metrics-grid">
  <MetricCard titulo="Temperatura Hornos" valor={ultimaTemp} icono="🔥" />
  <MetricCard titulo="Humedad Relativa" valor={ultimaHum} icono="💧" />
  <MetricCard titulo="Alertas Activas" valor={alertas.length.toString()} icono="🚨" />
</div>

<Card>
  <h2>Alertas sin Atender en Cocina</h2>
  <DataTable columnas={columnasAlertas} datos={alertas}>
    <div slot="acciones" let:fila>
      <span class="status-indicator">Sincronizado</span>
    </div>
  </DataTable>
</Card>

<style>
  .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 24px; }
  .status-indicator { font-size: 0.85rem; color: #64748b; font-style: italic; }
</style>