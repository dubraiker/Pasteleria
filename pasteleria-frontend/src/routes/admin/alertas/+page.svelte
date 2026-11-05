<script>
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import Button from '$lib/components/Button.svelte';
  import AlertMessage from '$lib/components/AlertMessage.svelte';

  let alertasSystem = [
    { id: 1, tipo: 'danger', titulo: 'Stock Crítico Detectado', detalle: 'El insumo "Cacao en Polvo 70%" está por debajo del mínimo (3 Kg restantes).', fecha: 'Hoy, 10:45 AM' },
    { id: 2, tipo: 'warning', titulo: 'Desconexión Temporal IoT', detalle: 'Pérdida de señal de 12 segundos en Báscula #02.', fecha: 'Hoy, 08:30 AM' },
    { id: 3, tipo: 'info', titulo: 'Respaldo de Base de Datos', detalle: 'Copia de seguridad realizada correctamente en la BD PostgreSQL local.', fecha: 'Ayer, 11:59 PM' }
  ];

  function resolverAlerta(id) {
    alertasSystem = alertasSystem.filter(a => a.id !== id);
  }
</script>

<div class="min-h-screen bg-slate-50 p-4 md:p-8">
  <Header 
    title="Panel Global de Alertas y Auditoría" 
    subtitle="Monitoreo central de incidencias de inventario, hardware IoT y logs del sistema"
  />

  <div class="flex justify-between items-center my-6">
    <span class="text-sm font-bold text-slate-700">Total Incidencias Activas: {alertasSystem.length}</span>
    <Button variant="outline" size="sm" on:click={() => window.location.reload()}>
      🔄 Actualizar Alertas
    </Button>
  </div>

  {#if alertasSystem.length === 0}
    <Card>
      <div class="text-center py-12">
        <span class="text-5xl">✅</span>
        <h3 class="text-xl font-bold text-slate-800 mt-3">Sin Alertas Pendientes</h3>
        <p class="text-slate-500 text-sm">Todas las variables del sistema y sensores IoT se encuentran en estado óptimo.</p>
      </div>
    </Card>
  {:else}
    <div class="space-y-4">
      {#each alertasSystem as alerta}
        <Card>
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div class="flex items-start gap-4">
              <div class="mt-1">
                <Badge type={alerta.tipo}>{alerta.titulo}</Badge>
              </div>
              <div>
                <p class="text-slate-800 font-medium text-sm">{alerta.detalle}</p>
                <span class="text-xs text-slate-400">{alerta.fecha}</span>
              </div>
            </div>
            <Button variant="secondary" size="sm" on:click={() => resolverAlerta(alerta.id)}>
              Marcar Resuelto
            </Button>
          </div>
        </Card>
      {/each}
    </div>
  {/if}
</div>