<script>
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import Button from '$lib/components/Button.svelte';

  let productos = [];
  let cargando = true;
  let productoSeleccionado = null;

  onMount(async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/productos/publico');
      if (res.ok) {
        productos = await res.json();
      } else {
        // Datos de respaldo para pruebas de interfaz si la base local no tiene productos
        productos = [
          { id: 1, nombre: 'Pastel de Chocolate Fudgy', categoria: 'Tortas', precio: 45000, descripcion: 'Bizcocho húmedo de cacao con ganache oscuro 70%.', disponible: true },
          { id: 2, nombre: 'Cheesecake de Frutos Rojos', categoria: 'Postres', precio: 38000, descripcion: 'Cremoso queso crema con mermelada artesanal.', disponible: true },
          { id: 3, nombre: 'Cupcakes de Vainilla y Fresa (x6)', categoria: 'Cupcakes', precio: 24000, descripcion: 'Esponjosos cupcakes con crema buttercream.', disponible: true },
          { id: 4, nombre: 'Tarta de Limón y Merengue', categoria: 'Tartas', precio: 32000, descripcion: 'Base crocante con curd de limón y merengue suizo.', disponible: false }
        ];
      }
    } catch (err) {
      console.error('Error cargando catálogo público local:', err);
    } finally {
      cargando = false;
    }
  });
</script>

<div class="min-h-screen bg-slate-50 flex flex-col">
  <!-- Navbar simplificado público -->
  <header class="bg-white border-b border-slate-200 px-6 py-4 flex justify-between items-center shadow-sm">
    <div class="flex items-center gap-2">
      <span class="text-2xl">🍰</span>
      <span class="font-extrabold text-xl text-slate-800">Pastelería IoT</span>
    </div>
    <div class="flex gap-3">
      <Button variant="outline" on:click={() => window.location.href = '/login'}>Iniciar Sesión</Button>
    </div>
  </header>

  <main class="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full">
    <Header title="Catálogo de Productos" subtitle="Descubre nuestros postres y productos recién horneados" />

    {#if cargando}
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
        {#each Array(4) as _}
          <div class="h-64 bg-slate-200 rounded-xl animate-pulse"></div>
        {/each}
      </div>
    {:else}
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mt-6">
        {#each productos as prod}
          <Card hoverable>
            <div class="h-40 bg-rose-50 rounded-lg flex items-center justify-center mb-4 text-5xl">
              🎂
            </div>
            <div class="flex justify-between items-start gap-2 mb-2">
              <h3 class="font-bold text-slate-800 text-lg leading-snug">{prod.nombre}</h3>
              <Badge type={prod.disponible ? 'success' : 'danger'}>
                {prod.disponible ? 'Disponible' : 'Agotado'}
              </Badge>
            </div>
            <p class="text-slate-500 text-xs mb-4 line-clamp-2">{prod.descripcion}</p>
            <div class="flex justify-between items-center pt-2 border-t border-slate-100">
              <span class="text-xl font-extrabold text-slate-900">${prod.precio.toLocaleString('es-CO')}</span>
              <Button variant="secondary" size="sm" on:click={() => productoSeleccionado = prod}>
                Ver Detalle
              </Button>
            </div>
          </Card>
        {/each}
      </div>
    {/if}
  </main>

  <!-- Modal Detalle de Producto -->
  {#if productoSeleccionado}
    <div class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl relative">
        <button on:click={() => productoSeleccionado = null} class="absolute top-4 right-4 text-slate-400 hover:text-slate-600 font-bold">✕</button>
        <div class="text-center mb-4">
          <span class="text-6xl">🎂</span>
          <h2 class="text-2xl font-bold text-slate-800 mt-2">{productoSeleccionado.nombre}</h2>
          <Badge type="info">{productoSeleccionado.categoria}</Badge>
        </div>
        <p class="text-slate-600 text-sm mb-6 text-center">{productoSeleccionado.descripcion}</p>
        <div class="bg-slate-50 p-4 rounded-xl flex justify-between items-center mb-6">
          <span class="text-slate-500 text-xs font-semibold">Precio unitario</span>
          <span class="text-2xl font-black text-rose-600">${productoSeleccionado.precio.toLocaleString('es-CO')}</span>
        </div>
        <Button variant="primary" fullWidth on:click={() => window.location.href = '/login'}>
          Iniciar Sesión para Encargar
        </Button>
      </div>
    </div>
  {/if}
</div>