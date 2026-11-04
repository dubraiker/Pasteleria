<script>
  import { iniciarSesion, registrarCliente } from '$lib/services/api_auth.js';
  import { usuarioSesion, tokenSesion } from '$lib/stores/authStore.js';
  import { goto } from '$app/navigation';
  import Card from '$lib/components/Card.svelte';
  import Header from '$lib/components/Header.svelte';
  import FormField from '$lib/components/FormField.svelte';
  import Button from '$lib/components/Button.svelte';
  import AlertMessage from '$lib/components/AlertMessage.svelte';

  
  let esRegistro = false;
  let mensajeError = '';
  let mensajeExito = '';
  let cargando = false;

 
  let correo = '';
  let password = '';
  let nombre = '';
  let apellido = '';

  function alternarModo() {
    esRegistro = !esRegistro;
    mensajeError = '';
    mensajeExito = '';
  }

  function redirigirPorRol(rol) {
    if (rol === 'Administrador') goto('/admin/usuarios');
    else if (rol === 'Pastelero') goto('/pastelero/inventario');
    else goto('/cliente/catalogo');
  }

  async function procesarFormulario() {
    mensajeError = '';
    mensajeExito = '';
    cargando = true;

    try {
      if (esRegistro) {
      
        await registrarCliente({ nombre, apellido, correo, password });
        mensajeExito = '¡Cuenta creada con éxito! Ahora puedes iniciar sesión.';
        esRegistro = false;
        password = '';
      } else {
       
        const respuesta = await iniciarSesion(correo, password);
        
      
        tokenSesion.set(respuesta.access_token);
        usuarioSesion.set(respuesta.usuario);

       
        redirigirPorRol(respuesta.usuario.rol);
      }
    } catch (err) {
      mensajeError = err.message;
    } finally {
      cargando = false;
    }
  }
</script>

<div class="auth-container">
  <Card>
    <Header 
      titulo={esRegistro ? 'Crear Cuenta de Cliente' : 'Iniciar Sesión'} 
      subtitulo={esRegistro ? 'Regístrate para explorar nuestro catálogo' : 'Ingresa tus credenciales para acceder al sistema'} 
    />

    <AlertMessage mensaje={mensajeError} tipo="error" />
    <AlertMessage mensaje={mensajeExito} tipo="success" />

    <form on:submit|preventDefault={procesarFormulario}>
      {#if esRegistro}
        <FormField label="Nombre" id="nombre">
          <input id="nombre" type="text" placeholder="Ej. Camilo" bind:value={nombre} required />
        </FormField>

        <FormField label="Apellido" id="apellido">
          <input id="apellido" type="text" placeholder="Ej. Andrés" bind:value={apellido} required />
        </FormField>
      {/if}

      <FormField label="Correo Electrónico" id="correo">
        <input id="correo" type="email" placeholder="usuario@pasteleria.com" bind:value={correo} required />
      </FormField>

      <FormField label="Contraseña" id="password">
        <input id="password" type="password" placeholder="••••••••" bind:value={password} required />
      </FormField>

      <div class="actions">
        <Button type="submit" variante="primary" disabled={cargando}>
          {cargando ? 'Procesando...' : (esRegistro ? 'Registrarme' : 'Ingresar')}
        </Button>

        <Button type="button" variante="secondary" on:click={alternarModo}>
          {esRegistro ? '¿Ya tienes cuenta? Inicia sesión' : '¿No tienes cuenta? Regístrate aquí'}
        </Button>
      </div>
    </form>
  </Card>
</div>

<style>
  .auth-container { max-width: 480px; margin: 40px auto; }
  input { padding: 10px 14px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; }
  input:focus { outline: none; border-color: #2563eb; }
  .actions { display: flex; flex-direction: column; gap: 10px; margin-top: 10px; }
</style>