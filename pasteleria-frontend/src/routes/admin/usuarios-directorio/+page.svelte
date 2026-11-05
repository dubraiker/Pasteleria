<script>
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import Button from '$lib/components/Button.svelte';

  let personal = [
    { id: 1, nombre: 'Camilo Andrés', cargo: 'Administrador de Sistema', area: 'Sistemas / TI', avatar: '👨‍💻', estado: 'En línea' },
    { id: 2, nombre: 'Julio Rodríguez', cargo: 'Pastelero Principal', area: 'Cocina / Producción', avatar: '👨‍🍳', estado: 'En línea' },
    { id: 3, nombre: 'Auxiliar Turno Mañana', cargo: 'Asistente de Insumos', area: 'Inventario IoT', avatar: '🥖', estado: 'Ausente' }
  ];
</script>

<div class="min-h-screen bg-slate-50 p-4 md:p-8">
  <Header 
    title="Directorio del Personal" 
    subtitle="Vista rápida del equipo de trabajo y roles asignados"
  />

  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
    {#each personal as p}
      <Card hoverable>
        <div class="flex items-center gap-4 mb-4">
          <div class="w-14 h-14 bg-rose-100 rounded-2xl flex items-center justify-center text-3xl shadow-sm">
            {p.avatar}
          </div>
          <div>
            <h3 class="font-bold text-slate-800 text-lg">{p.nombre}</h3>
            <p class="text-xs font-semibold text-rose-600">{p.cargo}</p>
          </div>
        </div>

        <div class="bg-slate-50 p-3 rounded-xl mb-4 space-y-1 text-xs">
          <div class="flex justify-between text-slate-500">
            <span>Área:</span>
            <span class="font-bold text-slate-700">{p.area}</span>
          </div>
          <div class="flex justify-between items-center text-slate-500">
            <span>Estado:</span>
            <Badge type={p.estado === 'En línea' ? 'success' : 'warning'}>{p.estado}</Badge>
          </div>
        </div>

        <Button variant="outline" size="sm" fullWidth on:click={() => alert(`Contactando a ${p.nombre}`)}>
          💬 Contactar
        </Button>
      </Card>
    {/each}
  </div>
</div>