<script>
  import { onMount } from 'svelte';
  import { obtenerProductos } from '$lib/services/api_productos.js';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';

  let productos = [];
  let cargando = true;

  onMount(async () => {
    try {
      productos = await obtenerProductos();
    } catch (e) {
      console.error('Error al cargar el catálogo:', e);
    } finally {
      cargando = false;
    }
  });
</script>

<Header 
  titulo="Catálogo Público de Repostería" 
  subtitulo="Descubre nuestra variedad de productos horneados diariamente con la máxima frescura" 
/>

{#if cargando}
  <p>Cargando vitrina de productos...</p>
{:else}
  <div class="grid-catalogo">
    {#each productos as producto}
      <Card>
        <div class="item-card">
          <span class="icon">🍰</span>
          <h3>{producto.nombre}</h3>
          <p class="desc">{producto.descripcion || 'Sin descripción disponible'}</p>
          <div class="precio-tag">${Number(producto.precio).toLocaleString('es-CO')} COP</div>
        </div>
      </Card>
    {/each}
  </div>
{/if}

<style>
  .grid-catalogo {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 20px;
    margin-top: 20px;
  }
  .item-card {
    text-align: center;
    padding: 10px;
  }
  .icon {
    font-size: 3rem;
    display: block;
    margin-bottom: 12px;
  }
  h3 {
    margin: 8px 0;
    color: #0f172a;
    font-size: 1.15rem;
  }
  .desc {
    font-size: 0.9rem;
    color: #64748b;
    margin: 8px 0 16px 0;
    min-height: 40px;
  }
  .precio-tag {
    font-size: 1.2rem;
    font-weight: 700;
    color: #d97706;
    background: #fef3c7;
    padding: 6px 12px;
    border-radius: 20px;
    display: inline-block;
  }
</style>