<script>
  export let variante = 'primary'; // 'primary', 'secondary', 'danger', 'success'
  export let type = 'button';
  export let disabled = false;
</script>

<button {type} {disabled} class="btn {variante}" on:click>
  <slot />
</button>

<style>
  .btn { padding: 10px 18px; border: none; border-radius: 8px; font-weight: 500; font-size: 0.9rem; cursor: pointer; transition: background 0.2s; }
  .btn:disabled { opacity: 0.5; cursor: not-allowed; }
  .primary { background: #2563eb; color: white; }
  .primary:hover:not(:disabled) { background: #1d4ed8; }
  .secondary { background: #64748b; color: white; }
  .secondary:hover:not(:disabled) { background: #475569; }
  .danger { background: #dc2626; color: white; }
  .danger:hover:not(:disabled) { background: #b91c1c; }
  .success { background: #16a34a; color: white; }
  .success:hover:not(:disabled) { background: #15803d; }
</style>
