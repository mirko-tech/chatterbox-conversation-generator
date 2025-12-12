# Chatterbox Dialogue Generator - Web UI

This is the React frontend for the Chatterbox Dialogue Generator.

## Getting Started

### Prerequisites

- Node.js 18+ (recommended: 20 LTS)
- npm or yarn
- Backend API server running (see main README)

### Installation

```bash
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

The optimized build will be created in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
VITE_API_URL=http://localhost:8000
```

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **FastAPI** - Backend API (separate Python server)

## Project Structure

```
src/
├── api/              # API client and types
│   └── client.ts
├── components/       # React components
│   ├── DialogueEditor.tsx
│   ├── SettingsPanel.tsx
│   └── StatusDisplay.tsx
├── App.tsx           # Main app component
├── main.tsx          # Entry point
└── index.css         # Global styles
```

## Features

- Visual dialogue editor with syntax help
- Interactive settings panel with sliders
- Real-time generation status
- Download generated audio files
- Dark theme optimized for long sessions
- Responsive layout (mobile-friendly)
