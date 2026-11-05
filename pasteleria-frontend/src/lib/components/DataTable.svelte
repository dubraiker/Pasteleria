
<script>
  
  export let columnas = []; 
  export let datos = [];    
  
  let filtroBusqueda = '';
  let paginaActual = 1;
  let filasPorPagina = 5;

  // Filtrar datos en tiempo real según el buscador
  $: datosFiltrados = datos.filter(item => {
    return Object.values(item).some(val => 
      String(val).toLowerCase().includes(filtroBusqueda.toLowerCase())
    );
  });

  // Paginación
  $: totalPaginas = Math.ceil(datosFiltrados.length / filasPorPagina) || 1;
  $: datosPaginados = datosFiltrados.slice(
    (paginaActual - 1) * filasPorPagina, 
    paginaActual * filasPorPagina
  );

  function cambiarPagina(nuevaPagina) {
    if (nuevaPagina >= 1 && nuevaPagina <= totalPaginas) {
      paginaActual = nuevaPagina;
    }
  }
</script>

<div class="datatable-container">
  <!-- Cabecera con Buscador -->
  <div class="datatable-header">
    <div class="search-box">
      <input 
        type="text" 
        placeholder="Buscar registros..." 
        bind:value={filtroBusqueda} 
      />
    </div>
    <div class="info-results">
      Mostrando {datosPaginados.length} de {datosFiltrados.length} resultados
    </div>
  </div>

 
  <div class="table-responsive">
    <table>
      <thead>
        <tr>
          {#each columnas as col}
            <th>{col.label}</th>
          {/each}
          <th class="text-center">Acciones</th>
        </tr>
      </thead>
      <tbody>
        {#if datosPaginados.length === 0}
          <tr>
            <td colspan={columnas.length + 1} class="empty-state">
              No se encontraron registros disponibles.
            </td>
          </tr>
        {:else}
          {#each datosPaginados as fila (fila.id || fila.codigo_mac)}
            <tr>
              {#each columnas as col}
                <td>{fila[col.key] !== undefined ? fila[col.key] : '-'}</td>
              {/each}
              <td class="acciones-cell">
                
                <slot name="acciones" item={fila} />
              </td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>

  
  <div class="datatable-footer">
    <button 
      class="btn-page" 
      disabled={paginaActual === 1} 
      on:click={() => cambiarPagina(paginaActual - 1)}
    >
      Anterior
    </button>
    
    <span>Página {paginaActual} de {totalPaginas}</span>
    
    <button 
      class="btn-page" 
      disabled={paginaActual === totalPaginas} 
      on:click={() => cambiarPagina(paginaActual + 1)}
    >
      Siguiente
    </button>
  </div>
</div>

<style>
  .datatable-container {
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    overflow: hidden;
    margin-bottom: 24px;
    border: 1px solid #e2e8f0;
  }
  .datatable-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    background-color: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    flex-wrap: wrap;
    gap: 12px;
  }
  .search-box input {
    padding: 8px 14px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    width: 250px;
    font-size: 0.9rem;
  }
  .search-box input:focus {
    outline: none;
    border-color: #db2777;
  }
  .info-results {
    font-size: 0.85rem;
    color: #64748b;
  }
  .table-responsive {
    width: 100%;
    overflow-x: auto; 
  }
  table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    font-size: 0.95rem;
  }
  th, td {
    padding: 12px 20px;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
  }
  th {
    background-color: #f1f5f9;
    font-weight: 600;
    color: #1e293b;
  }
  tr:hover td {
    background-color: #fdf2f8; 
  }
  .empty-state {
    text-align: center;
    color: #94a3b8;
    padding: 30px;
  }
  .acciones-cell {
    white-space: nowrap;
  }
  .datatable-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 20px;
    background-color: #f8fafc;
    border-top: 1px solid #e2e8f0;
    font-size: 0.9rem;
    color: #475569;
  }
  .btn-page {
    padding: 6px 14px;
    background: white;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    color: #334155;
  }
  .btn-page:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  .btn-page:not(:disabled):hover {
    background-color: #f1f5f9;
    border-color: #94a3b8;
  }
</style>