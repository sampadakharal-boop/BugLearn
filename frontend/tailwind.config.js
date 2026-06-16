/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          black: '#0B1220',
          darker: '#0B1220',
          dark: '#111827',
          mid: '#1E293B',
          light: '#334155',
          border: '#1E293B',
          green: '#10b981',
          'green-dark': '#059669',
          red: '#ef4444',
          yellow: '#f59e0b',
          blue: '#3B82F6',
          purple: '#8B5CF6',
          orange: '#f97316',
          cyan: '#06B6D4',
        },
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
