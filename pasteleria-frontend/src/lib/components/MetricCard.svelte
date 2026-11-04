<script>
  export let titulo = '';
  export let valor = '';
  export let icono = '📊';
</script>

<div class="metric">
  <div class="icon">{icono}</div>
  <div class="details">
    <span class="title">{titulo}</span>
    <span class="value">{valor}</span>
  </div>
</div>

<style>
  .metric { display: flex; align-items: center; background: #f8fafc; padding: 16px; border-radius: 10px; border: 1px solid #e2e8f0; gap: 14px; }
  .icon { font-size: 2rem; }
  .details { display: flex; flex-direction: column; }
  .title { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
  .value { font-size: 1.4rem; font-weight: 700; color: #0f172a; }
</style>