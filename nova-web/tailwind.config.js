/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'nova-dark': '#0a0b10',
        'nova-panel': '#0f1117',
        'nova-card': '#11131d',
        'nova-stroke': '#1c2130',
        'nova-purple': '#9b8cff',
        'nova-pink': '#ff6b9d',
      },
    },
  },
  plugins: [],
};
