/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
    extend: {
      opacity: {
        '5': '0.05',
        '10': '0.1',
        '15': '0.15',
       }
    },
    theme: {
      screens: {
        'sm': '576px',
        'md': '960px',
        'slg': '1279px',
        'lg': '1440px',
      },
    }
  },
  plugins: [],
}