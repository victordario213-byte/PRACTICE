/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          green: "#39FF14",
          black: "#0D0D0D",
        },
      },
    },
  },
  plugins: [],
}
