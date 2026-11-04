<script>
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import DataTable from '$lib/components/DataTable.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import Button from '$lib/components/Button.svelte';
  import AlertMessage from '$lib/components/AlertMessage.svelte';
  import { actualizarUsuarioAPI } from '$lib/services/api_usuarios.js';

  let usuarios = [];
  let cargando = true;
  let usuarioSeleccionado = null;
  let mostrandoModal = false;
  let mensajeExito = '';
  let mensajeError = '';

  // Definición de columnas de la tabla
  const columnas = [
    { key: 'nombre_completo', label: 'Usuario' },
    { key: 'correo', label: 'Correo Electrónico' }
  ];

  // Mapeo de IDs de perfil a Nombres y Colores de Badge
  const mapaRoles = {
    1: { nombre: 'Administrador', tipoBadge: 'danger' },
    2: { nombre: 'Pastelero', tipoBadge: 'warning' },
    3: { nombre: 'Cliente', tipoBadge: 'info' }
  };

  async function cargarUsuarios() {
    cargando = true;
    try {
      const res = await fetch('/api/usuarios');
      if (res.ok) {
        const datos = await res.json();
        usuarios = datos.map(u => ({ 
          ...u, 
          nombre_completo: `${u.nombre} ${u.apellido}`,
          rol_info: mapaRoles[u.id_perfil] || { nombre: u.rol_nombre || 'Sin Rol', tipoBadge: 'secondary' }
        }));
      }
    } catch (e) {
      console.error(e);
    } finally {
      cargando = false;
    }
  }

  function abrirModalEdicion(usuario) {
    usuarioSeleccionado = { ...usuario };
    mostrandoModal = true;
    mensajeExito = '';
    mensajeError = '';
  }

  async function guardarCambios() {
    mensajeExito = '';
    mensajeError = '';
    try {
      await actualizarUsuarioAPI(usuarioSeleccionado.id, {
        nombre: usuarioSeleccionado.nombre,
        apellido: usuarioSeleccionado.apellido,
        correo: usuarioSeleccionado.correo,
        id_perfil: Number(usuarioSeleccionado.id_perfil),
        estado: usuarioSeleccionado.estado
      });
      mensajeExito = 'Usuario y rol actualizados con éxito';
      mostrandoModal = false;
      await cargarUsuarios();
    } catch (err) {
      mensajeError = err.message;
    }
  }

  onMount(cargarUsuarios);
</script>

<Header 
  titulo="Gestión de Usuarios y Roles" 
  subtitulo="Administración de credenciales y asignación de perfiles RBAC" 
/>

<AlertMessage mensaje={mensajeError} tipo="error" />
<AlertMessage mensaje={mensajeExito} tipo="success" />

<Card>
  {#if cargando}
    <p>Cargando lista de usuarios...</p>
  {:else}
    <DataTable {columnas} datos={usuarios}>
      <div slot="acciones" let:fila class="acciones-cell">
        <!-- En lugar de mostrar Activo/Inactivo, renderizamos el Badge con el Rol -->
        <Badge tipo={fila.rol_info.tipoBadge}>
          {fila.rol_info.nombre}
        </Badge>
        
        <Button variante="secondary" on:click={() => abrirModalEdicion(fila)}>
          ✏️ Editar
        </Button>
      </div>
    </DataTable>
  {/if}
</Card>

{#if mostrandoModal}
  <div class="modal-backdrop">
    <div class="modal-content">
      <h2>Editar Usuario</h2>
      <form on:submit|preventDefault={guardarCambios}>
        <label>
          Nombre:
          <input type="text" bind:value={usuarioSeleccionado.nombre} required />
        </label>
        
        <label>
          Apellido:
          <input type="text" bind:value={usuarioSeleccionado.apellido} required />
        </label>

        <label>
          Correo Electrónico:
          <input type="email" bind:value={usuarioSeleccionado.correo} required />
        </label>

        <label>
          Perfil / Rol Asignado:
          <select bind:value={usuarioSeleccionado.id_perfil}>
            <option value={1}>Administrador</option>
            <option value={2}>Pastelero</option>
            <option value={3}>Cliente</option>
          </select>
        </label>

        <label class="checkbox-label">
          <input type="checkbox" bind:checked={usuarioSeleccionado.estado} />
          Cuenta Activa
        </label>

        <div class="modal-actions">
          <Button variante="primary" type="submit">Guardar Cambios</Button>
          <Button variante="danger" on:click={() => mostrandoModal = false}>Cancelar</Button>
        </div>
      </form>
    </div>
  </div>
{/if}

<style>
  .acciones-cell { display: flex; align-items: center; gap: 12px; }
  .modal-backdrop { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
  .modal-content { background: white; padding: 24px; border-radius: 12px; width: 100%; max-width: 450px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
  form { display: flex; flex-direction: column; gap: 14px; margin-top: 14px; }
  label { font-size: 0.9rem; font-weight: 600; color: #334155; display: flex; flex-direction: column; gap: 4px; }
  input[type="text"], input[type="email"], select { padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.95rem; }
  .checkbox-label { flex-direction: row; align-items: center; gap: 8px; font-weight: normal; }
  .modal-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 10px; }
</style>