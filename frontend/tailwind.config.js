/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // ICTSI Colors
        ictsi: {
          primary: '#003366',
          secondary: '#0066CC',
          accent: '#00AAFF',
        },
        // iTracker Colors
        itracker: {
          primary: '#FF6600',
          secondary: '#FF9933',
          accent: '#FFCC00',
        },
        // CLIA Colors
        clia: {
          primary: '#006633',
          secondary: '#009966',
          accent: '#00CC66',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
