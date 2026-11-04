<script>
  export let columnas = []; // [{ key: 'nombre', label: 'Nombre del Producto' }]
  export let datos = [];
</script>

<div class="table-container">
  {#if datos.length === 0}
    <div class="empty-state">No se encontraron registros activos.</div>
  {:else}
    <table>
      <thead>
        <tr>
          {#each columnas as col}
            <th>{col.label}</th>
          {/each}
          <th class="text-right">Acciones</th>
        </tr>
      </thead>
      <tbody>
        {#each datos as fila}
          <tr>
            {#each columnas as col}
              <td>{fila[col.key] !== undefined ? fila[col.key] : '-'}</td>
            {/each}
            <td class="text-right">
              <slot name="acciones" {fila} />
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>

<style>
  .table-container { width: 100%; overflow-x: auto; border: 1px solid #e2e8f0; border-radius: 8px; }
  table { width: 100%; border-collapse: collapse; font-family: system-ui; text-align: left; }
  th { background: #f8fafc; color: #475569; padding: 12px 16px; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; border-bottom: 1px solid #e2e8f0; }
  td { padding: 12px 16px; border-bottom: 1px solid #f1f5f9; color: #1e293b; font-size: 0.95rem; }
  tr:hover { background: #f8fafc; }
  .text-right { text-align: right; }
  .empty-state { padding: 24px; text-align: center; color: #64748b; }
</style>