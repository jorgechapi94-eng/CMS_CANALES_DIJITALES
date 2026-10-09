/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'upec-green': {
          DEFAULT: '#006633',
          dark: '#004d26',
          light: '#00994d',
          50: '#e6f2ec',
          100: '#b3d9c6',
          200: '#80c0a0',
          300: '#4da67a',
          400: '#1a8d54',
          500: '#006633',
          600: '#005529',
          700: '#004420',
          800: '#003316',
          900: '#00220d',
        },
        'upec-yellow': {
          DEFAULT: '#FFCE00',
          dark: '#d4ab00',
          light: '#ffe14d',
          50: '#fff9e0',
          100: '#fff0b3',
          200: '#ffe780',
          300: '#ffde4d',
          400: '#ffd61a',
          500: '#FFCE00',
          600: '#d4ab00',
          700: '#aa8900',
          800: '#806600',
          900: '#554400',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
