// vite.config.js
import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import vueI18n from '@intlify/unplugin-vue-i18n/vite';
import viteImagemin from 'vite-plugin-imagemin';
import vuetify from 'vite-plugin-vuetify'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), 'VUE_APP_');

  return {
    define: {
      // حل مشكلة ReferenceError: process is not defined
      'process.env': env,
      'process.platform': JSON.stringify('win32'),
      'global': 'window', // حل لبعض المكتبات القديمة
    },
    envPrefix: 'VUE_APP_',
    plugins: [
      // ✅ الترتيب الصحيح: Vue أولاً ثم Vuetify
      vue(), 
      vuetify({ 
        autoImport: true 
      }),
      vueI18n({
        include: path.resolve(__dirname, './src/locales/**'),
      }),
      viteImagemin({
        gifsicle: { interlaced: true },
        optipng: { optimizationLevel: 5 },
        mozjpeg: { quality: 80 },
        pngquant: { quality: [0.8, 0.9], speed: 4 },
        svgo: {
          plugins: [
            { name: 'removeViewBox' },
            { name: 'removeEmptyAttrs', active: false },
          ],
        },
      }),
    ],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      port: 8080,
      proxy: {
        '/api/graphql': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api\/graphql/, '/graphql')
        },
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          secure: false
        }
      }
    },
    build: {
      chunkSizeWarningLimit: 1600,
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes('node_modules')) {
              return id.toString().split('node_modules/')[1].split('/')[0].toString();
            }
          },
        },
      },
    },
  };
});
