import { sveltekit } from '@sveltejs/kit/vite';
import adapter from '@sveltejs/adapter-auto';
import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
	plugins: [
		sveltekit({
			adapter: adapter()
		})
	],
	resolve: {
		alias: {
			'$lib': path.resolve('./src/lib'),
			'#lib': path.resolve('./src/lib')
		}
	}
});