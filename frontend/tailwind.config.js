/** @type {import('tailwindcss').Config} */
export default {
  important: true,
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#186F65',
       
      },
    },
  },
  plugins: [require("daisyui"), require("tailwind-scrollbar")({ nocompatible: true })],
  daisyui: {
    themes: false, 
  }
}

