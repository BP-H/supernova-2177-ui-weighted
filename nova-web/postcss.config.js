// File: postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}

// ============================================
// STEP 5: Create app/globals.css
// ============================================
// File: app/globals.css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-nova-dark text-white;
  }
}

@layer components {
  .nova-gradient {
    @apply bg-gradient-to-r from-nova-purple to-nova-pink;
  }
  
  .nova-card {
    @apply bg-nova-card border border-nova-stroke rounded-xl p-4;
  }
  
  .nova-button {
    @apply px-4 py-2 rounded-lg bg-nova-panel border border-nova-stroke hover:bg-nova-purple/20 transition-all duration-200;
  }
}
