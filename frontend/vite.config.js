import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import vueI18n from '@intlify/unplugin-vue-i18n/vite';
import viteImagemin from 'vite-plugin-imagemin';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), 'VUE_APP_');

  return {
    define: {
      'process.env': {
        ...env,
        NODE_ENV: JSON.stringify(mode),
        VUE_APP_VERSION: JSON.stringify(process.env.npm_package_version),
      },
      'process.platform': JSON.stringify('win32'),
    },
    envPrefix: 'VUE_APP_',
    plugins: [
      vue(),
      vueI18n({
        include: path.resolve(__dirname, './src/locales/**'),
      }),
      viteImagemin({
        gifsicle: {
          interlaced: true,
        },
        optipng: {
          optimizationLevel: 5,
        },
        mozjpeg: {
          quality: 80,
        },
        pngquant: {
          quality: [0.8, 0.9],
          speed: 4,
        },
        svgo: {
          plugins: [
            {
              name: 'removeViewBox',
            },
            {
              name: 'removeEmptyAttrs',
              active: false,
            },
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
