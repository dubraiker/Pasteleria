<script>
  import { onMount } from 'svelte';
  import { obtenerProductos, crearProducto, desactivarProducto } from '$lib/services/api_productos.js';
  import { tokenSesion } from '$lib/stores/authStore.js';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import DataTable from '$lib/components/DataTable.svelte';
  import FormField from '$lib/components/FormField.svelte';
  import Button from '$lib/components/Button.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import AlertMessage from '$lib/components/AlertMessage.svelte';

  let productos = [];
  let cargando = false;
  let mensajeError = '';
  let mensajeExito = '';

  let nombre = '';
  let descripcion = '';
  let precio = '';
  let stock_actual = '';
  let etiqueta_yolo = '';

  const columnas = [
    { key: 'nombre', label: 'Producto' },
    { key: 'descripcion', label: 'Descripción' },
    { key: 'precio', label: 'Precio ($)' },
    { key: 'stock_actual', label: 'Stock Disponible' },
    { key: 'etiqueta_yolo', label: 'Etiqueta Visión IA' }
  ];

  async function cargarInventario() {
    cargando = true;
    try {
      productos = await obtenerProductos();
    } catch (err) {
      mensajeError = err.message;
    } finally {
      cargando = false;
    }
  }

  onMount(cargarInventario);

  async function guardarProducto() {
    mensajeError = '';
    mensajeExito = '';
    try {
      await crearProducto({
        id_categoria: 1, // Categoría por defecto
        nombre,
        descripcion,
        precio: Number(precio),
        stock_actual: Number(stock_actual),
        etiqueta_yolo
      }, $tokenSesion);

      mensajeExito = 'Producto registrado en el inventario';
      nombre = ''; descripcion = ''; precio = ''; stock_actual = ''; etiqueta_yolo = '';
      await cargarInventario();
    } catch (err) {
      mensajeError = err.message;
    }
  }

  async function eliminarReg(producto) {
    if (!confirm(`¿Desactivar del inventario el producto "${producto.nombre}"?`)) return;
    try {
      await desactivarProducto(producto.id, $tokenSesion);
      mensajeExito = 'Producto retirado del catálogo activo';
      await cargarInventario();
    } catch (err) {
      mensajeError = err.message;
    }
  }
</script>

<Header 
  titulo="Control de Inventario y Productos" 
  subtitulo="Gestión de productos y stock monitoreado por cámaras con Visión Artificial YOLO" 
/>

<AlertMessage mensaje={mensajeError} tipo="error" />
<AlertMessage mensaje={mensajeExito} tipo="success" />

<Card>
  <h2>Registrar Nuevo Producto en Inventario</h2>
  <form on:submit|preventDefault={guardarProducto} class="form-grid">
    <FormField label="Nombre del Producto" id="prod_nombre">
      <input id="prod_nombre" type="text" placeholder="Ej. Pastel de Chocolate Elite" bind:value={nombre} required />
    </FormField>

    <FormField label="Precio (COP)" id="prod_precio">
      <input id="prod_precio" type="number" step="100" placeholder="Ej. 45000" bind:value={precio} required />
    </FormField>

    <FormField label="Stock Inicial" id="prod_stock">
      <input id="prod_stock" type="number" placeholder="Ej. 12" bind:value={stock_actual} required />
    </FormField>

    <FormField label="Etiqueta Visión IA (YOLO)" id="prod_yolo">
      <input id="prod_yolo" type="text" placeholder="Ej. pastel_chocolate" bind:value={etiqueta_yolo} required />
    </FormField>

    <div class="full-width">
      <FormField label="Descripción" id="prod_desc">
        <textarea id="prod_desc" rows="2" placeholder="Detalles de la preparación e ingredientes..." bind:value={descripcion}></textarea>
      </FormField>
    </div>

    <div class="full-width">
      <Button type="submit" variante="success">Guardar en Inventario</Button>
    </div>
  </form>
</Card>

<Card>
  <h2>Catálogo Actual de Inventario</h2>
  {#if cargando}
    <p>Cargando productos...</p>
  {:else}
    <DataTable {columnas} datos={productos}>
      <div slot="acciones" let:fila>
        {#if fila.stock_actual <= 3}
          <Badge tipo="danger">Stock Crítico</Badge>
        {:else}
          <Badge tipo="success">En Stock</Badge>
        {/if}
        <Button variante="danger" on:click={() => eliminarReg(fila)}>Retirar</Button>
      </div>
    </DataTable>
  {/if}
</Card>

<style>
  .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; }
  .full-width { grid-column: 1 / -1; }
  input, textarea { padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; width: 100%; box-sizing: border-box; }
</style>