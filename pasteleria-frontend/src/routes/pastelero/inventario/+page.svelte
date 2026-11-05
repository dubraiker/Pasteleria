<!-- src/routes/pastelero/inventario/+page.svelte -->
<script>
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import MetricCard from '$lib/components/MetricCard.svelte';
  import DataTable from '$lib/components/DataTable.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import Button from '$lib/components/Button.svelte';
  import AlertMessage from '$lib/components/AlertMessage.svelte';
  import { tokenSesion } from '$lib/stores/authStore.js';
  import { obtenerProductos } from '$lib/services/api_productos.js';

  // Declaramos la variable 'insumos' (y 'productos') para evitar 'insumos is not defined'
  let insumos = [];
  let cargando = true;
  let mensajeError = '';

  const columnas = [
    { key: 'nombre', label: 'Producto / Insumo' },
    { key: 'descripcion', label: 'Descripción' },
    { key: 'precio_formateado', label: 'Precio' },
    { key: 'estado_label', label: 'Estado' }
  ];

  async function cargarInventario() {
    cargando = true;
    mensajeError = '';

    try {
      // Consumo mediante la función del servicio api_productos.js
      const datos = await obtenerProductos();

      insumos = datos.map((item) => ({
        ...item,
        precio_formateado: `$${Number(item.precio || 0).toLocaleString('es-CO')} COP`,
        estado_label: item.estado ? 'Disponible' : 'Inactivo'
      }));
    } catch (e) {
      console.error('Error cargando inventario:', e);
      mensajeError = e.message || 'Error de conexión con el servidor local.';
      insumos = [];
    } finally {
      cargando = false;
    }
  }

  onMount(cargarInventario);

  // Expresión reactiva segura declarada en script
  $: totalProductos = insumos.length;
</script>

<div class="min-h-screen bg-slate-50 p-4 md:p-8">
  <Header 
    title="Panel de Inventario" 
    subtitle="Gestión operativa y monitoreo de materia prima y productos en cocina" 
  />

  {#if mensajeError}
    <div class="mb-6">
      <AlertMessage type="danger" message={mensajeError} dismissible />
    </div>
  {/if}

 

  <!-- Contenedor DataTable -->
  <Card>
    <div class="flex flex-col sm:flex-row justify-between items-center gap-4 mb-6">
      <div>
        <h2 class="text-xl font-bold text-slate-800">Control de Productos & Inventario</h2>
        <p class="text-xs text-slate-500">Listado actualizado de inventario disponible</p>
      </div>
      <div class="flex gap-2">
        <Button variant="outline" size="sm" on:click={cargarInventario}>
          🔄 Actualizar
        </Button>
      </div>
    </div>

    {#if cargando}
      <div class="py-12 text-center text-slate-500 animate-pulse">Cargando datos de inventario...</div>
    {:else}
      <DataTable {columnas} datos={insumos}>
        <div slot="acciones" let:item class="flex gap-2">
          <Badge type={item.estado ? 'success' : 'danger'}>
            {item.estado_label}
          </Badge>
        </div>
      </DataTable>
    {/if}
  </Card>
</div>

<style>
  :global(body) {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
  }
</style>