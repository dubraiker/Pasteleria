<script>
  export let tipo = 'info'; // 'success', 'warning', 'danger', 'info'
</script>

<span class="badge {tipo}">
  <slot />
</span>

<style>
  .badge { display: inline-block; padding: 4px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }
  .success { background: #dcfce7; color: #166534; }
  .warning { background: #fef3c7; color: #92400e; }
  .danger { background: #fee2e2; color: #991b1b; }
  .info { background: #e0f2fe; color: #075985; }
</style>