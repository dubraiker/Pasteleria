<script>
  import { loginAPI } from '$lib/services/api_auth.js';
  import { goto } from '$app/navigation';
  
  let correo = '';
  let password = '';
  let mensajeError = '';

  async function manejarLogin() {
    try {
      mensajeError = '';
      
      const data = await loginAPI(correo, password);
      
     
      localStorage.setItem('token', data.token);
      goto('/cliente/catalogo');
    } catch (err) {
      mensajeError = err.message;
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