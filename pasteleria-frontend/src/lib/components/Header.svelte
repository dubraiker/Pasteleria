<script>
  export let titulo = '';
  export let subtitulo = '';
</script>

<header class="header">
  <h1>{titulo}</h1>
  {#if subtitulo}<p>{subtitulo}</p>{/if}
</header>

<style>
  .header { margin-bottom: 24px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; }
  h1 { margin: 0; color: #0f172a; font-size: 1.8rem; }
  p { margin: 4px 0 0 0; color: #64748b; }
</style>