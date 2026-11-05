<script>
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import { page } from '$app/state';
  import { tokenSesion } from '$lib/stores/authStore.js';
  import { goto } from '$app/navigation';

  $: {
    if (typeof window !== 'undefined') {
      const ruta = page.url.pathname;
      const tieneToken = $tokenSesion || localStorage.getItem('token');
      const esRutaPublica = ['/login', '/', '/cliente/catalogo-publico'].includes(ruta);

      // Si no tiene token y no es ruta pública, redirige a login
      if (!tieneToken && !esRutaPublica) {
        goto('/login');
      }
    }
  }
</script>

<div class="app-layout">
  <Navbar />
  <main class="main-content">
    <slot />
  </main>
  <Footer />
</div>

<style>
  .app-layout {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #f8fafc;
    color: #0f172a;
  }
  .main-content {
    flex: 1;
    padding: 24px;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
  }
</style>