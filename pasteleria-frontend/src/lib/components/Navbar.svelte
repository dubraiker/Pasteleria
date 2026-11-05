<script>
  import { goto } from '$app/navigation';
  import { tokenSesion, usuarioSesion, cerrarSesion } from '$lib/stores/authStore.js';

  let usuario = null;
  let token = null;

  $: usuario = $usuarioSesion;
  $: token = $tokenSesion;

  // Respaldo de 3 módulos por rol en caso de que usuario.modulos no esté presente
  const MODULOS_POR_DEFECTO = {
    1: [
      { nombre: 'Usuarios y Roles', ruta: '/admin/usuarios' },
      { nombre: 'Inventario General', ruta: '/pastelero/inventario' },
      { nombre: 'Monitoreo IoT', ruta: '/pastelero/alertas' }
    ],
    2: [
      { nombre: 'Inventario & YOLO', ruta: '/pastelero/inventario' },
      { nombre: 'Alertas Cocina', ruta: '/pastelero/alertas' },
      { nombre: 'Sensores en Vivo', ruta: '/pastelero/alertas-estado' }
    ],
    3: [
      { nombre: 'Catálogo de Productos', ruta: '/cliente/catalogo' },
      { nombre: 'Vitrina Pública', ruta: '/cliente/catalogo-publico' },
      { nombre: 'Directorio Personal', ruta: '/admin/usuarios-directorio' }
    ]
  };

  $: modulosPermitidos = usuario?.modulos && usuario.modulos.length === 3
    ? usuario.modulos
    : (usuario ? MODULOS_POR_DEFECTO[usuario.id_perfil] || [] : []);

  function salir() {
    cerrarSesion();
    goto('/login');
  }
</script>

<nav class="navbar">
  <div class="navbar-brand">
    <span class="logo-icon">🧁</span>
    <span class="navbar-title">Pastelería Inteligente IoT</span>
  </div>

  <div class="navbar-links">
    <a href="/">Inicio</a>

    {#if token && usuario}
      <!-- Renderizado de los 3 módulos correspondientes al perfil -->
      {#each modulosPermitidos as modulo}
        <a href={modulo.ruta}>{modulo.nombre}</a>
      {/each}

      <span class="user-welcome">Hola, {usuario.nombre}</span>
      <button class="btn-salir" on:click={salir}>Salir</button>
    {:else}
      <a href="/login" class="btn-login">Iniciar Sesión</a>
    {/if}
  </div>
</nav>

<style>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #1e293b;
    color: white;
    padding: 14px 24px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  .navbar-brand {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: bold;
    font-size: 1.2rem;
  }
  .navbar-links {
    display: flex;
    align-items: center;
    gap: 18px;
  }
  .navbar-links a {
    color: #e2e8f0;
    text-decoration: none;
    font-size: 0.95rem;
  }
  .navbar-links a:hover {
    color: #f472b6;
  }
  .user-welcome {
    font-size: 0.9rem;
    color: #cbd5e1;
    border-left: 1px solid #475569;
    padding-left: 15px;
  }
  .btn-login {
    background-color: #db2777;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
  }
  .btn-salir {
    background-color: transparent;
    border: 1px solid #ef4444;
    color: #ef4444;
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
  }
  .btn-salir:hover {
    background-color: #ef4444;
    color: white;
  }
</style>