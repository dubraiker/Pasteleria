<script>
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';

  const contactos = [
    { cargo: 'Atención al Cliente y Pedidos', correo: 'camilo@pasteleria.com', telefono: '+57 300 123 4567' },
    { cargo: 'Jefe de Pastelería y Producción', correo: 'carlos.mendoza@pasteleria.com', telefono: '+57 301 987 6543' },
    { cargo: 'Soporte Técnico e Infraestructura IoT', correo: 'diana.suarez@pasteleria.com', telefono: '+57 302 456 7890' }
  ];
</script>

<Header 
  titulo="Directorio de Atención e Información" 
  subtitulo="Canales oficiales de contacto de nuestro personal de servicio y soporte" 
/>

<div class="grid-directorio">
  {#each contactos as contacto}
    <Card>
      <h3>{contacto.cargo}</h3>
      <p>📧 Email: <strong>{contacto.correo}</strong></p>
      <p>📞 Teléfono: <strong>{contacto.telefono}</strong></p>
    </Card>
  {/each}
</div>

<style>
  .grid-directorio { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 16px; }
  h3 { margin-top: 0; color: #1e293b; font-size: 1.1rem; }
  p { margin: 8px 0; color: #475569; font-size: 0.95rem; }
</style>