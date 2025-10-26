# Safety Agent Frontend

Modern React frontend for the Construction Safety Agent System built with Material UI and Apple design principles.

## Features

- **Clean Material UI Components**: Professional, polished UI using MUI component library
- **Apple-Inspired Design**: Minimal, elegant styling following Apple's design principles
- **Video Upload**: Drag-and-drop video upload with preview
- **Real-time Analysis**: Watch progress as video is analyzed
- **Interactive Metrics Dashboard**: 4-card summary with color-coded severity
- **Agent Trace Tree**: Expandable accordion view showing multi-agent execution
- **Tool Call Inspection**: View input/output for each tool execution
- **Download Reports**: Export event data, reports, and traces as JSON/text

## Tech Stack

- **React 18** with TypeScript
- **Material UI 5** - Component library
- **Emotion** - CSS-in-JS styling
- **Vite** - Fast build tool and dev server

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

Or with `pnpm`:
```bash
pnpm install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 3. Configure API URL

The frontend connects to the FastAPI backend at `http://localhost:8000` by default.

To change this, edit `src/App.tsx`:
```typescript
const API_URL = 'http://your-api-url:8000';
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── VideoUpload.tsx       # Video upload component
│   │   ├── MetricsCard.tsx       # Metric display card
│   │   └── AgentTraceTree.tsx    # Agent execution tree
│   ├── App.tsx                   # Main application
│   ├── main.tsx                  # Entry point with theme provider
│   ├── theme.ts                  # MUI custom theme
│   └── types.ts                  # TypeScript interfaces
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Components

### VideoUpload
Drag-and-drop file upload with video preview

**Props:**
- `onUpload: (file: File) => void` - Callback when video is selected
- `isAnalyzing: boolean` - Show loading state

### MetricsCard
Display key metrics with custom colors

**Props:**
- `label: string` - Metric label
- `value: string | number` - Metric value
- `color?: string` - Custom text color

### AgentTraceTree
Interactive tree view of agent execution

**Props:**
- `traces: AgentTrace[]` - Array of agent execution traces

## Customization

### Theme

Edit `src/theme.ts` to customize colors, typography, and component styles:

```typescript
export const theme = createTheme({
  palette: {
    primary: {
      main: '#0071e3',  // Apple blue
    },
    // ... more colors
  },
  typography: {
    fontFamily: '-apple-system, BlinkMacSystemFont, ...',
  },
});
```

### API URL

Change the API endpoint in `src/App.tsx`:
```typescript
const API_URL = process.env.VITE_API_URL || 'http://localhost:8000';
```

Then create `.env.local`:
```bash
VITE_API_URL=http://your-api.com
```

## Building for Production

### Build

```bash
npm run build
```

Output will be in `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

### Deploy

#### Vercel
```bash
npm install -g vercel
vercel
```

#### Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

#### Docker

Create `Dockerfile`:
```dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Create `nginx.conf`:
```nginx
server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

Build and run:
```bash
docker build -t safety-agent-frontend .
docker run -p 3000:80 safety-agent-frontend
```

## Development

### Linting

```bash
npm run lint
```

### Type Checking

```bash
npx tsc --noEmit
```

### Hot Module Replacement

Vite provides instant HMR. Just save your files and see changes immediately.

## Design Principles

Following Apple's design philosophy:

1. **Simplicity**: Clean, uncluttered interface
2. **Focus**: Clear visual hierarchy
3. **Typography**: San Francisco-inspired font stack
4. **Whitespace**: Generous spacing for readability
5. **Consistency**: Unified design language
6. **Accessibility**: Semantic HTML and ARIA labels

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari 14+

## Performance

- Code splitting with Vite
- Lazy loading for heavy components
- Optimized MUI imports
- Production builds < 300KB gzipped

## Troubleshooting

### Port Already in Use
Change port in `vite.config.ts`:
```typescript
export default defineConfig({
  server: {
    port: 3001,
  },
});
```

### CORS Errors
Ensure the FastAPI backend has CORS configured for your frontend URL.

### Build Errors
Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

## Contributing

When adding new components:
1. Use Material UI components as building blocks
2. Follow the established theme/color scheme
3. Add TypeScript interfaces for props
4. Keep components focused and reusable

## License

MIT
