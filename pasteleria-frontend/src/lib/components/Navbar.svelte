<script>
  import { usuarioSesion, tokenSesion } from '$lib/stores/authStore.js';
  import { goto } from '$app/navigation';

  function cerrarSesion() {
    usuarioSesion.set(null);
    tokenSesion.set('');
    goto('/login');
  }
</script>

<nav class="navbar">
  <div class="brand">
    <span class="icon">🍰</span> Pastelería Inteligente
  </div>

  <div class="links">
    {#if $usuarioSesion}
      <!-- Renderizado dinámico de los 3 módulos traídos directamente de la BD -->
      {#if $usuarioSesion.modulos && $usuarioSesion.modulos.length > 0}
        {#each $usuarioSesion.modulos as modulo}
          <a href={modulo.ruta}>{modulo.nombre}</a>
        {/each}
      {/if}
      
      <span class="user-badge">{$usuarioSesion.correo} ({$usuarioSesion.rol})</span>
      <button class="btn-logout" on:click={cerrarSesion}>Cerrar Sesión</button>
    {:else}
      <a href="/login">Iniciar Sesión</a>
    {/if}
  </div>
</nav>

<style>
  .navbar { display: flex; justify-content: space-between; align-items: center; background: #1e293b; color: white; padding: 14px 24px; font-family: system-ui; }
  .brand { font-size: 1.25rem; font-weight: bold; }
  .links { display: flex; align-items: center; gap: 16px; }
  .links a { color: #f1f5f9; text-decoration: none; font-size: 0.95rem; }
  .links a:hover { text-decoration: underline; color: #f59e0b; }
  .user-badge { background: #334155; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; color: #cbd5e1; }
  .btn-logout { background: #ef4444; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; }
  .btn-logout:hover { background: #dc2626; }
</style>