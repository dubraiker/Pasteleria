<script>
  import { onMount } from 'svelte';
  import { obtenerProductos } from '$lib/services/api_productos.js';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import DataTable from '$lib/components/DataTable.svelte';
  import Badge from '$lib/components/Badge.svelte';

  let productos = [];
  let cargando = true;

  const columnas = [
    { key: 'nombre', label: 'Producto' },
    { key: 'categoria_nombre', label: 'Categoría' },
    { key: 'stock_actual', label: 'Stock en Lote' },
    { key: 'etiqueta_yolo', label: 'Clase IA (YOLO)' }
  ];

  onMount(async () => {
    try {
      productos = await obtenerProductos();
    } catch (e) {
      console.error(e);
    } finally {
      cargando = false;
    }
  });
</script>

<Header 
  titulo="Control de Productos y Stock en Lote" 
  subtitulo="Supervisión técnica de repostería asistida por visión artificial (YOLO)" 
/>

<Card>
  {#if cargando}
    <p>Cargando inventario de producción...</p>
  {:else}
    <DataTable {columnas} datos={productos}>
      <div slot="acciones" let:fila>
        <Badge tipo={fila.stock_actual > 5 ? 'success' : 'danger'}>
          {fila.stock_actual > 5 ? 'Stock Óptimo' : 'Reabastecer'}
        </Badge>
      </div>
    </DataTable>
  {/if}
</Card>