# Frontend - AI Teacher React Application

Modern React 18 frontend for the AI Teacher platform with TypeScript, Redux, WebSocket support, and Tailwind CSS styling.

## 📋 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Development Guide](#development-guide)
- [Building for Production](#building-for-production)
- [Features](#features)
- [API Integration](#api-integration)
- [Troubleshooting](#troubleshooting)

## 🔧 Requirements

### System Dependencies

- **Node.js 18+** (official LTS)
- **npm 9+** or **yarn 4+** (package manager)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

### Backend Service

- Running FastAPI backend (see `backend/README.md`)
  - API should be accessible at `http://localhost:8000`
  - WebSocket should be accessible at `ws://localhost:8000`

## 📦 Installation

### Step 1: Navigate to Frontend Directory

```bash
cd agentic_ai_teacher_onica/frontend
```

### Step 2: Install Dependencies

```bash
# Using npm
npm install

# Or using yarn
yarn install

# Or using pnpm
pnpm install
```

This installs all dependencies from `package.json`:
- React 18
- TypeScript
- Redux Toolkit
- React Router
- Axios
- Tailwind CSS
- And more

### Step 3: Verify Installation

```bash
# Check Node version
node --version    # Should be 18+

# Check npm version
npm --version     # Should be 9+

# Install dependencies (if not already done)
npm install
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (or `.env.local` for local development):

```env
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws

# Application
VITE_APP_NAME=AI Teacher
VITE_APP_VERSION=1.0.0

# Debug Mode
VITE_DEBUG=true
```

### Configuration Guide

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000` | `https://api.example.com` |
| `VITE_WS_URL` | WebSocket URL | `ws://localhost:8000/ws` | `wss://api.example.com/ws` |
| `VITE_APP_NAME` | Application name | `AI Teacher` | Any string |
| `VITE_DEBUG` | Enable debug logging | `false` | `true` or `false` |

### Vite Configuration

The project uses Vite for fast development and building. Main config in `vite.config.ts`:

```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

This proxies API calls to the backend during development.

## ▶️ Running the Application

### Development Mode

```bash
# Start development server with hot reload
npm run dev

# Or with yarn
yarn dev

# Or with pnpm
pnpm dev
```

Expected output:
```
VITE v5.0.0  ready in 123 ms

➜  Local:   http://localhost:3000/
➜  press h to show help
```

Visit `http://localhost:3000` in your browser.

**Features:**
- Hot Module Replacement (HMR) - changes instantly
- Fast Refresh - preserves component state
- Source maps for debugging
- Fast rebuilds

### Build for Production

```bash
# Build optimized bundle
npm run build

# Or with yarn
yarn build

# Or with pnpm
pnpm build
```

Output files go to `dist/` directory:
- Minified JavaScript
- Optimized CSS
- Optimized images
- HTML entry point

### Preview Production Build

```bash
# Build then serve locally
npm run preview

# Visit http://localhost:4173
```

### Linting and Code Quality

```bash
# Run ESLint
npm run lint

# Format code with Prettier
npm run format

# Type checking
npm run type-check
```

## 📁 Project Structure

### Directory Layout

```
frontend/
├── src/
│   ├── components/              # React components
│   │   ├── auth/               # Login, Register
│   │   ├── chat/               # Chat UI
│   │   │   ├── ChatWindow.tsx   # Main chat display
│   │   │   ├── ChatMessage.tsx  # Message bubble
│   │   │   ├── MessageInput.tsx # Input form
│   │   │   └── ChatHistory.tsx  # Conversation list
│   │   ├── slides/             # Slide viewer
│   │   ├── layout/             # Layout components
│   │   └── common/             # Reusable components
│   │
│   ├── pages/                   # Page components
│   │   ├── AuthPage.tsx         # Login/Register page
│   │   ├── TeachingPage.tsx     # Main teaching interface
│   │   ├── DashboardPage.tsx    # Dashboard
│   │   └── NotFoundPage.tsx     # 404 page
│   │
│   ├── store/                   # Redux state management
│   │   ├── slices/             # Redux slices
│   │   │   ├── authSlice.ts
│   │   │   ├── chatSlice.ts
│   │   │   └── uiSlice.ts
│   │   ├── hooks.ts            # Redux hooks
│   │   └── store.ts            # Store configuration
│   │
│   ├── services/                # API & external services
│   │   ├── api.ts              # Axios HTTP client
│   │   ├── websocket.ts        # WebSocket service
│   │   ├── auth.service.ts     # Auth logic
│   │   └── chat.service.ts     # Chat logic
│   │
│   ├── hooks/                   # Custom React hooks
│   │   ├── useChat.ts          # Chat hook
│   │   ├── useAuth.ts          # Auth hook
│   │   └── useWebSocket.ts     # WebSocket hook
│   │
│   ├── types/                   # TypeScript type definitions
│   │   ├── models.ts           # Data models
│   │   ├── api.ts              # API types
│   │   └── index.ts            # Exported types
│   │
│   ├── utils/                   # Utility functions
│   │   ├── api.ts              # API utilities
│   │   ├── storage.ts          # Local storage helpers
│   │   ├── format.ts           # Formatting utilities
│   │   └── validators.ts       # Form validation
│   │
│   ├── styles/                  # Global styles
│   │   ├── globals.css         # Global CSS
│   │   ├── variables.css       # CSS variables
│   │   └── tailwind.css        # Tailwind imports
│   │
│   ├── App.tsx                 # Main app component
│   ├── main.tsx                # React entry point
│   └── index.html              # HTML template
│
├── public/                      # Static assets
│   ├── favicon.ico
│   ├── images/
│   └── ...
│
├── package.json                # NPM dependencies
├── tsconfig.json               # TypeScript config
├── vite.config.ts              # Vite config
├── tailwind.config.js          # Tailwind config
├── postcss.config.js           # PostCSS config
└── README.md                   # This file
```

### Key Files

| File | Purpose |
|------|---------|
| `src/main.tsx` | React app entry point |
| `src/App.tsx` | Root component with routing |
| `src/index.html` | HTML template |
| `package.json` | Dependencies and scripts |
| `tsconfig.json` | TypeScript configuration |
| `vite.config.ts` | Vite build configuration |

## 💻 Development Guide

### State Management (Redux)

Store structure using Redux Toolkit:

```typescript
// Access state in component
const { user, isLoading } = useAppSelector(state => state.auth);

// Dispatch actions
const dispatch = useAppDispatch();
dispatch(loginUser({ email, password }));

// Use hooks (recommended)
const { user } = useAuth();
```

### Routing

Routes are defined in `App.tsx` using React Router:

```typescript
- /login          → Login/Register page
- /teaching       → Main teaching interface
- /dashboard      → User dashboard
- /404            → Not found page
```

Navigate using:

```typescript
const navigate = useNavigate();
navigate('/teaching');
```

### API Communication

Make API calls using the `api` service:

```typescript
import { api } from '@/services/api';

// Get data
const conversations = await api.getConversations();

// Post data
await api.createConversation('New Conversation');

// With error handling
try {
  const user = await api.getCurrentUser();
} catch (error) {
  console.error('Failed to fetch user:', error);
}
```

### WebSocket Communication

Real-time chat via WebSocket:

```typescript
import { wsService } from '@/services/websocket';

// Connect to chat
await wsService.connect(authToken);

// Send message
wsService.sendMessage({
  conversationId: 1,
  content: 'Hello',
  slideId: 1,
});

// Listen for events
wsService.on('chat.response_chunk', (chunk) => {
  // Handle streaming response
});
```

### Custom Hooks

Use custom hooks for common logic:

```typescript
// Chat hook
const {
  messages,
  isLoading,
  sendMessage,
  createConversation
} = useChat(conversationId);

// Auth hook
const {
  user,
  isAuthenticated,
  login,
  logout,
  register
} = useAuth();
```

### TypeScript Types

Use TypeScript for type safety:

```typescript
// Define component props
interface ChatProps {
  conversationId: number;
  onMessageSent?: () => void;
}

export function Chat({ conversationId, onMessageSent }: ChatProps) {
  // Component implementation
}
```

## 🏗️ Building for Production

### Pre-Build Checklist

```bash
# Run tests
npm run test

# Lint code
npm run lint

# Type check
npm run type-check

# Build
npm run build

# Preview build output
npm run preview
```

### Environment Variables for Production

Create `.env.production`:

```env
VITE_API_URL=https://api.yourdomain.com
VITE_WS_URL=wss://api.yourdomain.com/ws
VITE_DEBUG=false
```

### Build Output

After running `npm run build`:

```
dist/
├── index.html          # Entry HTML
├── assets/
│   ├── app-HASH.js     # Main JavaScript
│   ├── vendor-HASH.js  # Vendor code
│   ├── style-HASH.css  # Compiled CSS
│   └── ...
└── public/             # Static assets
```

### Deployment

Deploy the `dist/` folder to any static host:

```bash
# Build
npm run build

# Copy dist/ to your hosting
# - Vercel: Connect GitHub repo
# - Netlify: Drag and drop dist/
# - AWS S3: aws s3 sync dist/ s3://bucket
# - Traditional server: scp -r dist/ user@host:/var/www/
```

## ✨ Features

### Authentication
- User registration and login
- JWT token-based auth
- Password reset (future)
- Session management

### Chat System
- Create/manage conversations
- Real-time message streaming
- Message history
- Conversation deletion

### Teaching Interface
- Slide viewer
- Chat sidebar with history
- Real-time AI responses
- Message indicators

### State Management
- Redux for global state
- Local component state for UI
- Async thunk for API calls
- Dev tools for debugging

### UI/UX
- Responsive design
- Tailwind CSS styling
- Dark mode support (configurable)
- Accessible components

## 🔌 API Integration

### Available Endpoints

#### Authentication
```
POST   /api/v1/auth/register      - Create account
POST   /api/v1/auth/login         - Login
GET    /api/v1/auth/me            - Get current user
POST   /api/v1/auth/refresh       - Refresh token
```

#### Chat
```
POST   /api/v1/chat/conversations      - Create conversation
GET    /api/v1/chat/conversations      - List conversations
GET    /api/v1/chat/conversations/{id} - Get conversation
POST   /api/v1/chat/message            - Send message
DELETE /api/v1/chat/conversations/{id} - Delete conversation
```

#### WebSocket
```
ws://localhost:8000/ws
- Connection requires auth token
- Events: chat.message, chat.response_chunk, error, etc.
```

### Error Handling

API errors are handled consistently:

```typescript
try {
  await api.login(email, password);
} catch (error) {
  if (error.response?.status === 401) {
    // Handle unauthorized
  } else if (error.response?.status === 500) {
    // Handle server error
  } else {
    // Handle other errors
  }
}
```

### Request Interceptors

Authorization token is automatically added to requests:

```typescript
// In services/api.ts
api.interceptors.request.use(config => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

## 🧪 Development Workflow

### Hot Reload / HMR

Changes to code automatically reload in the browser while preserving state:

```bash
# Terminal
npm run dev

# Make changes to src/components/chat/ChatWindow.tsx
# Browser automatically updates without full page reload
```

### Debugging

### Browser DevTools

1. Open all browser DevTools (F12)
2. Go to Sources tab
3. Find your file in the file tree
4. Set breakpoints and debug

### Redux DevTools

1. Install Redux DevTools browser extension
2. Open DevTools
3. Go to Redux tab
4. View dispatched actions and state changes

### Console Logging

```typescript
console.log('Debug info:', data);
console.error('Error:', error);
console.table(arrayOfObjects);
```

## 📺 Testing Locally

### Test Login Flow

```bash
# 1. Start backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# 2. Start frontend
cd frontend
npm run dev

# 3. Open http://localhost:3000
# 4. Register a new user
# 5. Login
# 6. Navigate to teaching page
# 7. Create a conversation
# 8. Send a message
```

### Test WebSocket

Check browser console for WebSocket messages:

```javascript
// In browser console
ws = new WebSocket('ws://localhost:8000/ws?token=YOUR_TOKEN');
ws.onmessage = (event) => console.log('WS:', event.data);
ws.send(JSON.stringify({type: 'chat.message', content: 'Hello'}));
```

## 🔧 Troubleshooting

### Node/npm Issue

```
npm: command not found
```

**Fix:**
```bash
# Install Node.js 18+
# From https://nodejs.org/

# Verify installation
node --version
npm --version
```

### Dependencies Won't Install

```
npm ERR! code ERESOLVE
```

**Fix:**
```bash
# Clear npm cache
npm cache clean --force

# Delete lockfile and node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Port 3000 Already in Use

```
EADDRINUSE: address already in use :::3000
```

**Fix:**
```bash
# Change port in vite.config.ts:
server: {
  port: 3001,  // Use different port
}

# Or kill existing process
lsof -ti:3000 | xargs kill -9
```

### API Connection Errors

```
Failed to fetch from API
```

**Check:**
1. Backend is running (`http://localhost:8000`)
2. `VITE_API_URL` in `.env` is correct
3. No CORS issues (check browser console)
4. API responds to `http://localhost:8000/health`

### WebSocket Connection Failures

```
WebSocket connection failed
```

**Check:**
1. Backend WebSocket handler is running
2. Auth token is valid
3. `VITE_WS_URL` in `.env` is correct
4. No firewall blocking WebSocket (port 8000)

### Build Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear build cache
rm -rf dist/

# Rebuild
npm run build
```

### TypeScript Errors

```bash
# Run type check to find errors
npm run type-check

# Fix common issues:
# - Missing type definitions
# - Type mismatches
# - Unused variables
```

## 📚 Learning Resources

- [React 18 Docs](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Redux Toolkit](https://redux-toolkit.js.org/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Vite Guide](https://vitejs.dev/guide/)
- [Axios Documentation](https://axios-http.com/docs/intro)

## 🤝 Contributing

To contribute to the frontend:

1. Create a feature branch
2. Follow TypeScript best practices
3. Use proper component structure
4. Test your changes
5. Submit a pull request

## 📄 License

See LICENSE file in project root.

## 🎯 Next Steps

1. ✅ Install Node.js and dependencies
2. ✅ Configure environment variables
3. ✅ Ensure backend is running
4. ✅ Start frontend dev server
5. ✅ Test login and chat functionality
6. ⏭️ Customize styling and branding
7. ⏭️ Deploy to production

## 🚀 Common Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint

# Type check
npm run type-check

# Format code
npm run format
```

---

**Need help?** Check the main [README.md](../README.md) for overall project documentation.
