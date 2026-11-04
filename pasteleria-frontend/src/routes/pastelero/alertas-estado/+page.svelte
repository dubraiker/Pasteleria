<script>
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import Badge from '$lib/components/Badge.svelte';

  const estadosFrescura = [
    { producto: 'Croissant de Almendras', estado: 'Recién Horneado', hora: 'Hace 15 min' },
    { producto: 'Tarta Holandesa de Manzana', estado: 'En Horno', hora: 'Listo en 10 min' },
    { producto: 'Pastel Tiramisú Supremo', estado: 'Refrigerado', hora: 'Temperatura 4°C' },
    { producto: 'Cheesecake de Frutos Rojos', estado: 'Recién Horneado', hora: 'Hace 5 min' }
  ];
</script>

<Header 
  titulo="Estado de Productos Frescos" 
  subtitulo="Monitoreo de horneado en tiempo real y disponibilidad de productos" 
/>

<Card>
  <h2>Horneado y Frescura en Vitrina</h2>
  <div class="lista-estados">
    {#each estadosFrescura as item}
      <div class="estado-row">
        <div>
          <strong>{item.producto}</strong>
          <span class="hora">{item.hora}</span>
        </div>
        <Badge tipo={item.estado === 'En Horno' ? 'warning' : 'success'}>
          {item.estado}
        </Badge>
      </div>
    {/each}
  </div>
</Card>

<style>
  .lista-estados { display: flex; flex-direction: column; gap: 12px; margin-top: 12px; }
  .estado-row { display: flex; justify-content: space-between; align-items: center; padding: 12px; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0; }
  .hora { display: block; font-size: 0.8rem; color: #64748b; margin-top: 2px; }
</style>