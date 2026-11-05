<script>
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import Button from '$lib/components/Button.svelte';

  let pesoEscala1 = 14.85; // kg
  let temperaturaPr = 18.5; // °C
  let humedadPr = 62; // %
  let estadoModulo = 'OK';
  let buscando = false;

  function simularLectura() {
    buscando = true;
    setTimeout(() => {
      pesoEscala1 = Number((14.00 + Math.random() * 2).toFixed(2));
      temperaturaPr = Number((17.5 + Math.random() * 2).toFixed(1));
      humedadPr = Math.floor(60 + Math.random() * 5);
      buscando = false;
    }, 600);
  }

  onMount(() => {
    const interval = setInterval(simularLectura, 10000); // Polling cada 10 seg
    return () => clearInterval(interval);
  });
</script>

<div class="min-h-screen bg-slate-50 p-4 md:p-8">
  <Header 
    title="Telemetría y Sensores IoT" 
    subtitle="Lectura en tiempo real de básculas pesadoras HX711 y variables ambientales"
  />

  <div class="flex justify-between items-center my-6">
    <div class="flex items-center gap-2">
      <span class="w-3 h-3 bg-emerald-500 rounded-full animate-ping"></span>
      <span class="text-sm font-semibold text-slate-700">Conexión IoT Activa (Local)</span>
    </div>
    <Button variant="outline" size="sm" on:click={simularLectura} loading={buscando}>
      ⚡ Forzar Lectura
    </Button>
  </div>

  <!-- Cards de Sensores -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
    <!-- Sensor Pesaje HX711 -->
    <Card>
      <div class="flex justify-between items-start mb-4">
        <div>
          <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Báscula #01 - Harina</span>
          <h3 class="text-lg font-bold text-slate-800">Celda HX711</h3>
        </div>
        <Badge type="success">En Línea</Badge>
      </div>
      <div class="text-center py-4 bg-slate-50 rounded-xl mb-4">
        <span class="text-4xl font-extrabold text-slate-900">{pesoEscala1}</span>
        <span class="text-sm font-bold text-slate-500"> Kg</span>
      </div>
      <p class="text-xs text-slate-500 text-center">Última tara: Hace 12 minutos</p>
    </Card>

    <!-- Sensor Temperatura -->
    <Card>
      <div class="flex justify-between items-start mb-4">
        <div>
          <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Cámara Fría</span>
          <h3 class="text-lg font-bold text-slate-800">Temperatura</h3>
        </div>
        <Badge type={temperaturaPr > 22 ? 'danger' : 'info'}>
          {temperaturaPr > 22 ? 'Elevada' : 'Normal'}
        </Badge>
      </div>
      <div class="text-center py-4 bg-slate-50 rounded-xl mb-4">
        <span class="text-4xl font-extrabold text-slate-900">{temperaturaPr}</span>
        <span class="text-sm font-bold text-slate-500"> °C</span>
      </div>
      <p class="text-xs text-slate-500 text-center">Rango óptimo: 15°C - 20°C</p>
    </Card>

    <!-- Sensor Humedad -->
    <Card>
      <div class="flex justify-between items-start mb-4">
        <div>
          <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Almacén Seco</span>
          <h3 class="text-lg font-bold text-slate-800">Humedad Relativa</h3>
        </div>
        <Badge type="success">Estable</Badge>
      </div>
      <div class="text-center py-4 bg-slate-50 rounded-xl mb-4">
        <span class="text-4xl font-extrabold text-slate-900">{humedadPr}</span>
        <span class="text-sm font-bold text-slate-500"> %</span>
      </div>
      <p class="text-xs text-slate-500 text-center">Humedad de aire controlada</p>
    </Card>
  </div>
</div>