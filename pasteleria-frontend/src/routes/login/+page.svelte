<!-- src/routes/login/+page.svelte -->
<script>
  import { tokenSesion, usuarioSesion } from '$lib/stores/authStore.js';
  import { goto } from '$app/navigation';

  let correo = '';
  let password = '';
  let mensajeError = '';
  let cargando = false;

  async function ejecutarLogin(e) {
    // Evita explícitamente cualquier recarga del navegador
    if (e) e.preventDefault();
    
    if (!correo || !password) {
      mensajeError = 'Por favor completa todos los campos.';
      return;
    }

    cargando = true;
    mensajeError = '';

    try {
      // Petición directa a FastAPI (pasa por el proxy de Vite)
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ correo, password })
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Correo o contraseña incorrectos');
      }

      const datos = await res.json();

      // Guardar token y usuario en los stores reactivos
      tokenSesion.set(datos.access_token);
      usuarioSesion.set(datos.usuario);

      const perfil = Number(datos.usuario.id_perfil);

      // Redirección a las rutas existentes en las carpetas de tu proyecto
      if (perfil === 1) {
        await goto('/admin/usuarios');
      } else if (perfil === 2) {
        await goto('/pastelero/alertas-estado');
      } else {
        await goto('/cliente/catalogo-publico');
      }
    } catch (error) {
      mensajeError = error.message;
    } finally {
      cargando = false;
    }
  }
</script>

<div class="login-container">
  <div class="login-card">
    <h2>Pastelería Inteligente IoT</h2>
    <p>Ingresa tus credenciales para acceder al sistema</p>

    <!-- Usamos event modifier preventDefault en la etiqueta form -->
    <form on:submit|preventDefault={ejecutarLogin}>
      <div class="campo">
        <label for="correo">Correo Electrónico</label>
        <input 
          id="correo" 
          type="email" 
          placeholder="camilo@pasteleria.com" 
          bind:value={correo} 
          required 
        />
      </div>

      <div class="campo">
        <label for="password">Contraseña</label>
        <input 
          id="password" 
          type="password" 
          placeholder="••••••••" 
          bind:value={password} 
          required 
        />
      </div>

      {#if mensajeError}
        <div class="alert-error">
          {mensajeError}
        </div>
      {/if}

      <!-- type="button" desactiva por completo el submit nativo del navegador -->
      <button 
        type="button" 
        class="btn-ingresar" 
        on:click={ejecutarLogin} 
        disabled={cargando}
      >
        {cargando ? 'Verificando...' : 'Ingresar'}
      </button>
    </form>
  </div>
</div>

<style>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 75vh;
  }
  .login-card {
    background: #ffffff;
    padding: 32px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    width: 100%;
    max-width: 400px;
  }
  .login-card h2 {
    color: #db2777;
    margin-top: 0;
    text-align: center;
  }
  .login-card p {
    text-align: center;
    color: #64748b;
    font-size: 0.9rem;
    margin-bottom: 24px;
  }
  .campo {
    display: flex;
    flex-direction: column;
    margin-bottom: 18px;
  }
  label {
    font-weight: 600;
    margin-bottom: 6px;
    font-size: 0.9rem;
    color: #334155;
  }
  input {
    padding: 10px 14px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 1rem;
    outline: none;
  }
  input:focus {
    border-color: #db2777;
  }
  .alert-error {
    background-color: #fee2e2;
    color: #991b1b;
    padding: 10px;
    border-radius: 6px;
    font-size: 0.85rem;
    margin-bottom: 16px;
    text-align: center;
  }
  .btn-ingresar {
    width: 100%;
    padding: 12px;
    background-color: #db2777;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  .btn-ingresar:hover:not(:disabled) {
    background-color: #be185d;
  }
  .btn-ingresar:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
</style>