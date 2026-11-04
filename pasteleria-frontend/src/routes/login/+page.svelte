<script>
  import { usuarioSesion, tokenSesion } from '$lib/stores/authStore.js';
  import { goto } from '$app/navigation';
  import Card from '$lib/components/Card.svelte';
  import FormField from '$lib/components/FormField.svelte';
  import Button from '$lib/components/Button.svelte';
  import AlertMessage from '$lib/components/AlertMessage.svelte';

  let correo = '';
  let password = '';
  let mensajeError = '';
  let cargando = false;

  async function iniciarSesion() {
    mensajeError = '';
    cargando = true;
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ correo, password })
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error al iniciar sesión');

      tokenSesion.set(data.access_token);
      usuarioSesion.set(data.usuario);

      // Redirige al primer módulo que retornó la base de datos para ese rol
      if (data.usuario.modulos && data.usuario.modulos.length > 0) {
        goto(data.usuario.modulos[0].ruta);
      } else {
        goto('/');
      }
    } catch (err) {
      mensajeError = err.message;
    } finally {
      cargando = false;
    }
  }
</script>

<div class="login-wrapper">
  <Card>
    <h2>Iniciar Sesión</h2>
    <p class="subtitle">Pastelería Inteligente & Monitoreo IoT</p>

    <AlertMessage mensaje={mensajeError} tipo="error" />

    <form on:submit|preventDefault={iniciarSesion}>
      <FormField label="Correo Electrónico">
        <input type="email" bind:value={correo} required placeholder="ejemplo@pasteleria.com" />
      </FormField>

      <FormField label="Contraseña">
        <input type="password" bind:value={password} required placeholder="••••••••" />
      </FormField>

      <Button variante="primary" disabled={cargando}>
        {cargando ? 'Autenticando...' : 'Ingresar al Sistema'}
      </Button>
    </form>
  </Card>
</div>

<style>
  .login-wrapper { max-width: 400px; margin: 60px auto; }
  .subtitle { color: #64748b; font-size: 0.9rem; margin-bottom: 20px; }
  input { width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; }
</style>