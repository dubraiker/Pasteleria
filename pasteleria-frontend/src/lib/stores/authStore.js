
import { writable } from 'svelte/store';


const isBrowser = typeof window !== 'undefined';

const initialToken = isBrowser ? localStorage.getItem('token') : null;
const initialUsuario = isBrowser ? JSON.parse(localStorage.getItem('usuario') || 'null') : null;

export const tokenSesion = writable(initialToken);
export const usuarioSesion = writable(initialUsuario);

if (isBrowser) {
  tokenSesion.subscribe((val) => {
    if (val) localStorage.setItem('token', val);
    else localStorage.removeItem('token');
  });

  usuarioSesion.subscribe((val) => {
    if (val) localStorage.setItem('usuario', JSON.stringify(val));
    else localStorage.removeItem('usuario');
  });
}

export function cerrarSesion() {
  tokenSesion.set(null);
  usuarioSesion.set(null);
  if (isBrowser) {
    localStorage.clear();
  }
}