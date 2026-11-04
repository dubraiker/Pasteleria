<script>
  import { onMount } from 'svelte';
  import { obtenerAlertasPendientes, atenderAlerta } from '$lib/services/api_iot.js';
  import { usuarioSesion } from '$lib/stores/authStore.js';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import DataTable from '$lib/components/DataTable.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import Button from '$lib/components/Button.svelte';
  import AlertMessage from '$lib/components/AlertMessage.svelte';

  let alertas = [];
  let cargando = false;
  let mensajeExito = '';
  let mensajeError = '';

  const columnas = [
    { key: 'dispositivo_nombre', label: 'Dispositivo IoT' },
    { key: 'tipo_alerta_nombre', label: 'Tipo de Alerta' },
    { key: 'mensaje', label: 'Detalle del Evento' },
    { key: 'nivel_riesgo', label: 'Nivel de Riesgo' }
  ];

  async function cargarAlertas() {
    cargando = true;
    try {
      alertas = await obtenerAlertasPendientes();
    } catch (err) {
      mensajeError = err.message;
    } finally {
      cargando = false;
    }
  }

  // Refresco automático cada 5 segundos para simular tiempo real
  onMount(() => {
    cargarAlertas();
    const intervalo = setInterval(cargarAlertas, 5000);
    return () => clearInterval(intervalo);
  });

  async function procesarAtencion(alerta) {
    mensajeExito = '';
    mensajeError = '';
    try {
      await atenderAlerta(alerta.id, $usuarioSesion.id);
      mensajeExito = 'Alerta marcada como atendida exitosamente';
      await cargarAlertas();
    } catch (err) {
      mensajeError = err.message;
    }
  }
</script>

<Header 
  titulo="Alertas de Emergencia y Control Ambiental (IoT)" 
  subtitulo="Monitoreo de sobrecalentamiento, incendios e intrusiones sincronizado en tiempo real" 
/>

<AlertMessage mensaje={mensajeError} tipo="error" />
<AlertMessage mensaje={mensajeExito} tipo="success" />

<Card>
  <h2>Alertas Pendientes por Atención</h2>
  {#if cargando && alertas.length === 0}
    <p>Consultando sensores IoT...</p>
  {:else}
    <DataTable {columnas} datos={alertas}>
      <div slot="acciones" let:fila>
        <Badge tipo={fila.nivel_riesgo === 'CRITICO' ? 'danger' : (fila.nivel_riesgo === 'ALTO' ? 'warning' : 'info')}>
          {fila.nivel_riesgo}
        </Badge>
        <Button variante="success" on:click={() => procesarAtencion(fila)}>Atender Emergencia</Button>
      </div>
    </DataTable>
  {/if}
</Card>