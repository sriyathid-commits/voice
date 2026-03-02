# Voice for Bharat - Web Frontend

This is the Next.js 15 web frontend for Voice for Bharat, a voice-first, AI-powered application that democratizes access to government welfare information across India.

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Data Fetching**: React Query (@tanstack/react-query)
- **PWA**: next-pwa (to be configured)
- **Hosting**: AWS Amplify (production), Vercel (preview)

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Update .env.local with your configuration
```

### Development

```bash
# Run development server
npm run dev

# Open http://localhost:3000
```

### Build

```bash
# Create production build
npm run build

# Start production server
npm start
```

### Other Commands

```bash
# Type checking
npm run type-check

# Linting
npm run lint
```

## Project Structure

```
src/
├── app/                    # Next.js 15 app directory
│   ├── (dashboard)/       # Dashboard routes
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # React components
│   └── ui/               # Base UI components
├── lib/                   # Utilities and helpers
│   └── constants.ts      # App constants
├── hooks/                 # Custom React hooks
├── store/                 # Zustand stores
│   ├── authStore.ts      # Authentication state
│   └── uiStore.ts        # UI state
└── types/                 # TypeScript types
    └── index.ts          # Type definitions
```

## Environment Variables

See `.env.example` for required environment variables:

- `NEXT_PUBLIC_API_URL`: Backend API endpoint
- `NEXT_PUBLIC_WS_URL`: WebSocket endpoint
- `NEXT_PUBLIC_CLOUDFRONT_URL`: CloudFront CDN URL
- `NEXT_PUBLIC_COGNITO_USER_POOL_ID`: AWS Cognito User Pool ID
- `NEXT_PUBLIC_COGNITO_CLIENT_ID`: AWS Cognito Client ID

## Features

- ✅ Next.js 15 with App Router
- ✅ TypeScript with strict mode
- ✅ Tailwind CSS with custom color palette
- ✅ Zustand for state management
- ✅ React Query ready for data fetching
- ✅ PWA manifest configured
- ✅ Responsive design (mobile-first)
- ✅ Accessibility features (ARIA labels, keyboard navigation)
- ✅ Multilingual support structure (6 Indian languages)

## Color Palette

- **Primary Orange**: #ff6b35
- **Primary Green**: #4caf50
- **Primary Navy**: #1a2332
- **Success**: #4caf50
- **Warning**: #ffc107
- **Error**: #f44336
- **Info**: #9c27b0

## Supported Languages

- English (en)
- Hindi (hi)
- Marathi (mr)
- Kannada (kn)
- Tamil (ta)
- Telugu (te)

## License

Proprietary - Voice for Bharat
