import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const usuarioInicial = browser ? JSON.parse(localStorage.getItem('usuario_pasteleria') || 'null') : null;
const tokenInicial = browser ? localStorage.getItem('token_pasteleria') || '' : '';

export const usuarioSesion = writable(usuarioInicial);
export const tokenSesion = writable(tokenInicial);

if (browser) {
  usuarioSesion.subscribe((val) => {
    if (val) localStorage.setItem('usuario_pasteleria', JSON.stringify(val));
    else localStorage.removeItem('usuario_pasteleria');
  });

  tokenSesion.subscribe((val) => {
    if (val) localStorage.setItem('token_pasteleria', val);
    else localStorage.removeItem('token_pasteleria');
  });
}