<script>
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import DataTable from '$lib/components/DataTable.svelte';
  import Button from '$lib/components/Button.svelte';
  import AlertMessage from '$lib/components/AlertMessage.svelte';
  import FormField from '$lib/components/FormField.svelte';
  import { tokenSesion } from '$lib/stores/authStore.js';

  let usuarios = [];
  let cargando = true;
  let mensaje = null;
  let usuarioSeleccionado = null;

  const columnas = [
    { key: 'nombre_completo', label: 'Nombre Completo' },
    { key: 'correo', label: 'Correo Electrónico' },
    { key: 'perfil_nombre', label: 'Rol / Perfil' },
    { key: 'estado_label', label: 'Estado' }
  ];

  async function cargarUsuarios() {
    cargando = true;
    mensaje = null;

    try {
      const res = await fetch('/api/usuarios/', {
        headers: { 'Authorization': `Bearer ${$tokenSesion}` }
      });

      if (!res.ok) throw new Error('Error al obtener la lista de usuarios');

      const datosAPI = await res.json();

      usuarios = datosAPI
        .filter(u => u.estado !== false)
        .map((u) => ({
          ...u,
          nombre_completo: `${u.nombre || ''} ${u.apellido || ''}`.trim(),
          perfil_nombre: u.perfil_nombre || (u.id_perfil === 1 ? 'Administrador' : u.id_perfil === 2 ? 'Pastelero' : 'Cliente'),
          estado: u.estado !== undefined ? u.estado : true,
          estado_label: '🟢 Activo'
        }));
    } catch (e) {
      mensaje = { type: 'danger', text: e.message || 'Error de conexión.' };
      usuarios = [];
    } finally {
      cargando = false;
    }
  }

  onMount(cargarUsuarios);

  async function guardarCambios() {
    try {
      const partes = usuarioSeleccionado.nombre_completo.trim().split(' ');
      const nombre = partes[0] || '';
      const apellido = partes.slice(1).join(' ') || '';

      const payload = {
        nombre,
        apellido,
        correo: usuarioSeleccionado.correo,
        id_perfil: Number(usuarioSeleccionado.id_perfil),
        estado: true
      };

      const res = await fetch(`/api/usuarios/${usuarioSeleccionado.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${$tokenSesion}`
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('No se pudo actualizar el usuario');

      mensaje = { type: 'success', text: 'Usuario actualizado exitosamente.' };
      usuarioSeleccionado = null;
      await cargarUsuarios();
    } catch (err) {
      mensaje = { type: 'danger', text: err.message };
    }
  }

  async function eliminarUsuario(id) {
    if (!confirm('¿Estás seguro de eliminar este usuario del sistema?')) return;

    try {
      const res = await fetch(`/api/usuarios/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${$tokenSesion}` }
      });

      if (!res.ok) throw new Error('Error al eliminar el usuario');

      mensaje = { type: 'success', text: 'Usuario eliminado correctamente.' };
      await cargarUsuarios();
    } catch (err) {
      mensaje = { type: 'danger', text: err.message };
    }
  }
</script>

<div class="min-h-screen bg-slate-50 p-4 md:p-8">
  <Header 
    title="Administración de Usuarios" 
    subtitle="Gestión de accesos, roles y control de cuentas" 
  />

  {#if mensaje}
    <div class="mb-6">
      <AlertMessage type={mensaje.type} message={mensaje.text} dismissible on:dismiss={() => mensaje = null} />
    </div>
  {/if}

  <Card>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold text-slate-800">Cuentas Registradas</h2>
      <Button variant="primary" size="sm" on:click={cargarUsuarios}>🔄 Refrescar</Button>
    </div>

    {#if cargando}
      <div class="py-12 text-center text-slate-500 animate-pulse">Cargando directorio...</div>
    {:else}
      <DataTable {columnas} datos={usuarios}>
        <div slot="acciones" let:item class="flex gap-2">
          <Button variant="outline" size="sm" on:click={() => usuarioSeleccionado = { ...item }}>
            ✏️ Editar
          </Button>
          <Button variant="danger" size="sm" on:click={() => eliminarUsuario(item.id)}>
            🗑️ Eliminar
          </Button>
        </div>
      </DataTable>
    {/if}
  </Card>

  <!-- Modal de Edición (Ventana Flotante / Popup Central) -->
  {#if usuarioSeleccionado}
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl relative">
        <button on:click={() => usuarioSeleccionado = null} class="absolute top-4 right-4 text-slate-400 hover:text-slate-600 font-bold text-lg">✕</button>
        <h3 class="text-xl font-bold text-slate-800 mb-4">Editar Usuario</h3>
        
        <div class="space-y-4">
          <FormField label="Nombre Completo" bind:value={usuarioSeleccionado.nombre_completo} />
          <FormField label="Correo Electrónico" bind:value={usuarioSeleccionado.correo} type="email" />
          
          <div class="flex flex-col gap-1">
            <label for="perfil" class="text-sm font-semibold text-slate-700">Rol / Perfil</label>
            <select id="perfil" bind:value={usuarioSeleccionado.id_perfil} class="w-full p-3 rounded-xl border border-slate-200 bg-white text-slate-800 font-medium">
              <option value={1}>1 - Administrador</option>
              <option value={2}>2 - Pastelero</option>
              <option value={3}>3 - Cliente</option>
            </select>
          </div>

          <div class="pt-4 flex gap-2">
            <Button variant="outline" fullWidth on:click={() => usuarioSeleccionado = null}>Cancelar</Button>
            <Button variant="primary" fullWidth on:click={guardarCambios}>Guardar Cambios</Button>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>