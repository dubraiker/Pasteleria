<script>
  import { onMount } from 'svelte';
  import { usuarioSesion } from '$lib/stores/authStore.js';
  import { goto } from '$app/navigation';

  onMount(() => {
    if (!$usuarioSesion) {
      goto('/login');
    } else {
      const rol = $usuarioSesion.rol;
      if (rol === 'Administrador') goto('/admin/usuarios');
      else if (rol === 'Pastelero') goto('/pastelero/inventario');
      else goto('/cliente/catalogo');
    }
  });
</script>

<div class="loading-screen">
  <p>Cargando módulo asignado...</p>
</div>

<style>
  .loading-screen { text-align: center; padding: 60px; color: #64748b; font-size: 1.1rem; }
</style>