<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { tokenSesion, usuarioSesion } from '$lib/stores/authStore.js';

  onMount(() => {
    if (!$tokenSesion || !$usuarioSesion) {
      goto('/login');
    } else {
      const perfil = $usuarioSesion.id_perfil;
      if (perfil === 1) goto('/admin/usuarios');
      else if (perfil === 2) goto('/pastelero/alertas-estado');
      else goto('/cliente/catalogo-publico');
    }
  });
</script>

<div style="text-align: center; padding: 50px;">
  <p>Cargando módulo asignado...</p>
</div>