/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'primary': {
          100: '#E7D9FB', // Lightest shade
          200: '#CFB3F7',
          300: '#B78CF3',
          400: '#9F66EF',
          500: '#9768EA', // Base color
          600: '#7D4EC8',
          700: '#643BA7',
          800: '#4B2885',
          900: '#321563'  // Darkest shade
        }
      }
    },
  },
  plugins: [],
};