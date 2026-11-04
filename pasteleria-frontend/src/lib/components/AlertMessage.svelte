<script>
  export let mensaje = '';
  export let tipo = 'error'; // 'error', 'success'
</script>

{#if mensaje}
  <div class="alert {tipo}">
    {mensaje}
  </div>
{/if}

<style>
  .alert { padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; font-size: 0.9rem; }
  .error { background: #fef2f2; border: 1px solid #fca5a5; color: #991b1b; }
  .success { background: #f0fdf4; border: 1px solid #86efac; color: #166534; }
</style>