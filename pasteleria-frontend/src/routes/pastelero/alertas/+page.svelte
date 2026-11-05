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
      const datos = await obtenerAlertasPendientes();
      // Mapeo seguro asegurando que nivel_riesgo exista siempre
      alertas = (datos || []).map((a) => ({
        ...a,
        nivel_riesgo: a.nivel_riesgo || 'MEDIO',
        dispositivo_nombre: a.dispositivo_nombre || 'Dispositivo IoT',
        tipo_alerta_nombre: a.tipo_alerta_nombre || 'Alerta General'
      }));
    } catch (err) {
      mensajeError = err.message || 'Error al obtener alertas pendientes';
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
      await atenderAlerta(alerta.id, $usuarioSesion?.id || 1);
      mensajeExito = 'Alerta marcada como atendida exitosamente';
      await cargarAlertas();
    } catch (err) {
      mensajeError = err.message || 'Error al procesar la atención';
    }
  }
</script>

<div class="p-4 md:p-8 space-y-6">
  <Header 
    title="Alertas de Emergencia y Control Ambiental (IoT)" 
    subtitle="Monitoreo de sobrecalentamiento, incendios e intrusiones sincronizado en tiempo real" 
  />

  {#if mensajeError}
    <AlertMessage message={mensajeError} type="danger" dismissible on:dismiss={() => mensajeError = ''} />
  {/if}

  {#if mensajeExito}
    <AlertMessage message={mensajeExito} type="success" dismissible on:dismiss={() => mensajeExito = ''} />
  {/if}

  <Card>
    <div class="mb-4">
      <h2 class="text-xl font-bold text-slate-800">Alertas Pendientes por Atención</h2>
      <p class="text-xs text-slate-500">Eventos críticos registrados por los sensores ESP32</p>
    </div>

    {#if cargando && alertas.length === 0}
      <p class="py-8 text-center text-slate-500 animate-pulse">Consultando sensores IoT...</p>
    {:else}
      <!-- 🟢 Usamos let:item para que coincida con el slot de DataTable.svelte -->
      <DataTable {columnas} datos={alertas}>
        <div slot="acciones" let:item class="flex items-center gap-2">
          <Badge type={item?.nivel_riesgo === 'CRITICO' || item?.nivel_riesgo === 'ALTO' ? 'danger' : 'info'}>
            {item?.nivel_riesgo || 'GENERAL'}
          </Badge>
          <Button variant="primary" size="sm" on:click={() => procesarAtencion(item)}>
            Atender Emergencia
          </Button>
        </div>
      </DataTable>
    {/if}
  </Card>
</div>