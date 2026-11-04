<script>
  import { onMount } from 'svelte';
  import { obtenerProductos } from '$lib/services/api_productos.js';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import Button from '$lib/components/Button.svelte';

  let productos = [];
  let cargando = false;

  async function cargarCatalogo() {
    cargando = true;
    try {
      productos = await obtenerProductos();
    } catch (err) {
      console.error(err);
    } finally {
      cargando = false;
    }
  }

  onMount(cargarCatalogo);
</script>

<Header 
  titulo="Catálogo de Repostería Inteligente" 
  subtitulo="Explora nuestros productos frescos disponibles en tiempo real" 
/>

{#if cargando}
  <p>Cargando catálogo...</p>
{:else if productos.length === 0}
  <Card><p>No hay productos disponibles por el momento.</p></Card>
{:else}
  <div class="grid-catalogo">
    {#each productos as producto}
      <Card>
        <div class="card-content">
          <div class="badge-row">
            <Badge tipo={producto.stock_actual > 0 ? 'success' : 'danger'}>
              {producto.stock_actual > 0 ? 'Disponible' : 'Agotado'}
            </Badge>
          </div>
          <h3>{producto.nombre}</h3>
          <p class="desc">{producto.descripcion || 'Elaborado con ingredientes frescos de la más alta calidad.'}</p>
          <div class="price-row">
            <span class="price">${Number(producto.precio).toLocaleString('es-CO')} COP</span>
            <Button variante="primary" disabled={producto.stock_actual <= 0}>Ordenar</Button>
          </div>
        </div>
      </Card>
    {/each}
  </div>
{/if}

<style>
  .grid-catalogo { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
  .card-content { display: flex; flex-direction: column; height: 100%; justify-content: space-between; }
  .badge-row { margin-bottom: 8px; }
  h3 { margin: 0 0 8px 0; color: #1e293b; font-size: 1.2rem; }
  .desc { color: #64748b; font-size: 0.9rem; margin-bottom: 16px; flex-grow: 1; }
  .price-row { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 12px; }
  .price { font-size: 1.25rem; font-weight: bold; color: #16a34a; }
</style>