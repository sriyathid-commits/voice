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
        primary: {
          orange: '#ff6b35',
          green: '#4caf50',
          navy: '#1a2332',
        },
        status: {
          success: '#4caf50',
          warning: '#ffc107',
          error: '#f44336',
          info: '#9c27b0',
        },
        card: {
          'light-blue': '#e3f2fd',
          'light-orange': '#fff3e0',
        },
      },
      fontSize: {
        'header-title': '18px',
        'header-subtitle': '12px',
        'tab-label': '14px',
        'metric-number': '32px',
        'card-title': '14px',
        'status-item': '16px',
        'guide-text': '14px',
        'footer-link': '12px',
        'primary-cta': '18px',
        'secondary-cta': '16px',
      },
      height: {
        'btn-primary': '56px',
        'btn-secondary': '48px',
      },
      minHeight: {
        'touch-target': '44px',
      },
      minWidth: {
        'touch-target': '44px',
      },
      borderRadius: {
        'card': '12px',
      },
      spacing: {
        'card-padding': '20px',
      },
    },
  },
  plugins: [],
}
