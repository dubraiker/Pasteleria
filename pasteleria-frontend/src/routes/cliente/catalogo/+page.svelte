<script>
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import Button from '$lib/components/Button.svelte';
  import AlertMessage from '$lib/components/AlertMessage.svelte';
  import { usuarioSesion, tokenSesion } from '$lib/stores/authStore.js';

  let productos = [];
  let cargando = true;
  let mensajeExito = '';

  onMount(async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/productos', {
        headers: { Authorization: `Bearer ${$tokenSesion}` }
      });
      if (res.ok) {
        productos = await res.json();
      }
    } catch (e) {
      console.error(e);
    } finally {
      cargando = false;
    }
  });

  function agregarAlCarrito(producto) {
    mensajeExito = `¡${producto.nombre} agregado a tu pedido!`;
    setTimeout(() => mensajeExito = '', 3000);
  }
</script>

<div class="min-h-screen bg-slate-50 p-4 md:p-8">
  <Header title="Catálogo Exclusivo" subtitle={`Bienvenido, ${$usuarioSesion?.nombre || 'Cliente'}`} />

  {#if mensajeExito}
    <div class="mb-4">
      <AlertMessage type="success" message={mensajeExito} dismissible />
    </div>
  {/if}

  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
    {#each productos as prod}
      <Card hoverable>
        <div class="flex justify-between items-start mb-3">
          <Badge type="info">{prod.categoria}</Badge>
          <span class="text-lg font-black text-slate-800">${prod.precio}</span>
        </div>
        <h3 class="font-bold text-slate-800 text-xl mb-2">{prod.nombre}</h3>
        <p class="text-slate-500 text-sm mb-4">{prod.descripcion}</p>
        <Button variant="primary" size="sm" fullWidth on:click={() => agregarAlCarrito(prod)}>
          + Añadir a Pedido
        </Button>
      </Card>
    {/each}
  </div>
</div>