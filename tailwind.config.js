/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
    extend: {},
    theme: {
      screens: {
        'sm': '576px',
        'md': '960px',
        'lg': '1440px',
      },
    }
  },
  plugins: [],
}