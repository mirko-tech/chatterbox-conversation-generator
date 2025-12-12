/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#0f1419',
          surface: '#1a1f2e',
          border: '#2d3548',
          text: '#e6edf3',
          muted: '#8b949e',
        },
      },
    },
  },
  plugins: [],
}
