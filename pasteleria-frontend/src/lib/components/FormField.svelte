<script>
  export let label = '';
  export let id = '';
</script>

<div class="field">
  <label for={id}>{label}</label>
  <slot />
</div>

<style>
  .field { display: flex; flex-direction: column; margin-bottom: 14px; }
  label { font-size: 0.85rem; font-weight: 600; color: #334155; margin-bottom: 6px; }
</style>