/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
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
      animation: {
        'glow': 'glow 2s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(155, 140, 255, 0.5)' },
          '100%': { boxShadow: '0 0 30px rgba(155, 140, 255, 0.8)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
      },
    },
  },
  plugins: [],
}
