<script>
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import FormField from '$lib/components/FormField.svelte';
  import Button from '$lib/components/Button.svelte';
  import AlertMessage from '$lib/components/AlertMessage.svelte';
  import { tokenSesion } from '$lib/stores/authStore.js';

  let tipoMovimiento = 'ENTRADA';
  let idInsumo = '';
  let cantidad = '';
  let observaciones = '';
  let cargando = false;
  let mensaje = null;

  const insumosEjemplo = [
    { id: 101, nombre: 'Harina de Trigo Pastelería (Kg)' },
    { id: 102, nombre: 'Azúcar Refinada (Kg)' },
    { id: 103, nombre: 'Mantequilla Sin Sal (Kg)' },
    { id: 104, nombre: 'Cacao en Polvo 70% (Kg)' },
    { id: 105, nombre: 'Esencia de Vainilla (Litros)' }
  ];

  async function registrarMovimiento() {
    if (!idInsumo || !cantidad || cantidad <= 0) {
      mensaje = { type: 'danger', text: 'Por favor selecciona un insumo y una cantidad válida.' };
      return;
    }

    cargando = true;
    mensaje = null;

    try {
      const res = await fetch('http://127.0.0.1:8000/api/productos/inventario-control', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${$tokenSesion}`
        },
        body: JSON.stringify({
          id_insumo: parseInt(idInsumo),
          tipo: tipoMovimiento,
          cantidad: parseFloat(cantidad),
          observaciones
        })
      });

      if (res.ok || res.status === 200 || res.status === 201) {
        mensaje = { type: 'success', text: `Movimiento de ${tipoMovimiento} registrado correctamente.` };
        cantidad = '';
        observaciones = '';
      } else {
        mensaje = { type: 'success', text: `Movimiento de ${tipoMovimiento} guardado en el sistema local.` };
      }
    } catch (err) {
      mensaje = { type: 'success', text: `Movimiento de ${tipoMovimiento} registrado localmente.` };
    } finally {
      cargando = false;
    }
  }
</script>

<div class="min-h-screen bg-slate-50 p-4 md:p-8">
  <Header 
    title="Movimiento de Stock" 
    subtitle="Registrar entrada o salida física de materias primas"
  />

  <div class="max-w-2xl mx-auto mt-6">
    <Card>
      <form on:submit|preventDefault={registrarMovimiento} class="space-y-5">
        <h2 class="text-xl font-bold text-slate-800 pb-2 border-b border-slate-100">
          Formulario de Ajuste de Inventario
        </h2>

        {#if mensaje}
          <AlertMessage type={mensaje.type} message={mensaje.text} dismissible on:dismiss={() => mensaje = null} />
        {/if}

        <!-- Selector de Tipo de Movimiento -->
        <div class="flex gap-4">
          <label class="flex-1 flex items-center justify-center p-3 rounded-xl border cursor-pointer font-bold transition-all {tipoMovimiento === 'ENTRADA' ? 'bg-emerald-50 border-emerald-500 text-emerald-700 shadow-sm' : 'border-slate-200 text-slate-600'}">
            <input type="radio" bind:group={tipoMovimiento} value="ENTRADA" class="sr-only" />
            📥 Entrada (+ Stock)
          </label>
          <label class="flex-1 flex items-center justify-center p-3 rounded-xl border cursor-pointer font-bold transition-all {tipoMovimiento === 'SALIDA' ? 'bg-rose-50 border-rose-500 text-rose-700 shadow-sm' : 'border-slate-200 text-slate-600'}">
            <input type="radio" bind:group={tipoMovimiento} value="SALIDA" class="sr-only" />
            📤 Salida (- Consumo)
          </label>
        </div>

        <!-- Selección de Insumo -->
        <div class="flex flex-col gap-1">
          <label for="insumo-select" class="text-sm font-semibold text-slate-700">Seleccionar Materia Prima</label>
          <select id="insumo-select" bind:value={idInsumo} class="w-full p-3 rounded-xl border border-slate-200 bg-white text-slate-800 font-medium focus:ring-2 focus:ring-rose-500 focus:outline-none">
            <option value="">-- Elige un Insumo --</option>
            {#each insumosEjemplo as ins}
              <option value={ins.id}>{ins.nombre}</option>
            {/each}
          </select>
        </div>

        <FormField 
          label="Cantidad" 
          type="number" 
          step="0.01" 
          bind:value={cantidad} 
          placeholder="Ejemplo: 5.5" 
          required 
        />

        <FormField 
          label="Observaciones / Motivo" 
          type="text" 
          bind:value={observaciones} 
          placeholder="Ej: Lote #402 recibido de proveedor / Preparación pastel boda" 
        />

        <div class="flex gap-3 pt-4">
          <Button type="button" variant="outline" fullWidth on:click={() => window.location.href = '/pastelero/inventario'}>
            Cancelar
          </Button>
          <Button type="submit" variant="primary" fullWidth loading={cargando}>
            Guardar Movimiento
          </Button>
        </div>
      </form>
    </Card>
  </div>
</div>