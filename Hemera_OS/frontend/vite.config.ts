import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
// REMOVA: import { componentTagger } from "lovable-tagger";

export default defineConfig({
  server: {
    host: "::",
    port: 8080,
  },
  plugins: [
    react(),
    // REMOVA: componentTagger(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});