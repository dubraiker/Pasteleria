<script>
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
</script>

<div class="app-layout">
  <Navbar />
  <main class="main-content">
    <slot />
  </main>
  <Footer />
</div>

<style>
  :global(body) { margin: 0; font-family: system-ui, -apple-system, sans-serif; background: #f8fafc; color: #0f172a; }
  .app-layout { min-height: 100vh; display: flex; flex-direction: column; }
  .main-content { flex: 1; width: 92%; max-width: 1100px; margin: 24px auto; }
</style>