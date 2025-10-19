# Frontend Application

A modern React TypeScript application built with Vite, featuring a comprehensive UI component library, authentication, multi-tenant support, and AI chat capabilities.

## 🎯 Overview

This frontend application provides a complete user interface for the full-stack template, featuring:

- **Modern React 19** with TypeScript for type safety and latest React features
- **Vite 7** for lightning-fast development and optimized builds
- **Tailwind CSS 4** with native Vite integration and shadcn/ui components
- **React Router 7** for modern client-side navigation and routing
- **Biome** for ultra-fast linting and formatting (ESLint/Prettier alternative)
- **AI SDK** for seamless AI chat integration with streaming responses
- **WebAuthn** for passwordless authentication and enhanced security
- **React Hook Form** with Zod validation for robust form handling
- **Auto-generated API clients** from backend OpenAPI specifications
- **Zustand** for lightweight and flexible state management
- **nuqs** for type-safe URL state management and query parameters
- **Advanced UI Components** including data tables, charts, carousels, and more

## 🏗️ Project Structure

```
src/
├── api/                   # Auto-generated API client
│   ├── models/            # TypeScript models from backend
│   ├── services/          # API service classes
│   └── core/              # Core API utilities
├── components/
│   ├── features/         # Feature-specific components
│   │   ├── ai-chat/      # AI chat interface
│   │   ├── auth/         # Authentication components
│   │   ├── dashboard/    # Dashboard components
│   │   ├── profile/      # User profile management
│   │   ├── roles/        # Role management
│   │   ├── tenant/       # Tenant management
│   │   └── users/        # User management
│   ├── layouts/          # Page layout components
│   │   ├── default-layout.tsx
│   │   └── dashboard-sidebar-layout.tsx
│   ├── providers/        # React context providers
│   │   └── auth-provider.tsx
│   ├── shared/           # Reusable components
│   │   ├── footer.tsx
│   │   ├── loading.tsx
│   │   └── list-*.tsx
│   ├── ui/               # shadcn/ui base components
│   └── ai-elements/      # Vercel ai-elements components
├── hooks/                # Custom React hooks
├── lib/                  # Utility functions
│   ├── utils.ts         # General utilities
│   └── image-utils.ts   # Image processing utilities
└── assets/              # Static assets
```

## 🚀 Getting Started

### Prerequisites

- Node.js 22+ 
- pnpm (recommended) or npm
- Backend API running on `http://localhost:8000`

### Installation

1. **Install Dependencies**:
   ```bash
   pnpm install
   ```

2. **Generate API Client** (Backend must be running):
   ```bash
   pnpm run generate:api
   ```

3. **Start Development Server**:
   ```bash
   pnpm dev
   ```

   The application will be available at: http://localhost:3000

## 📜 Available Scripts

```bash
# Development
pnpm dev                    # Start development server (port 3000)
pnpm build                  # Build for production (TypeScript + Vite)
pnpm preview                # Preview production build
pnpm type-check             # Run TypeScript type checking

# Code Quality
pnpm lint                   # Run Biome linter
pnpm lint:fix               # Run Biome linter with auto-fix
pnpm format                 # Format code with Biome

# API Integration
pnpm run generate:api       # Generate TypeScript API client from backend
```

## ⚙️ Configuration

### Vite Configuration

The `vite.config.ts` includes:

- **Development Server**: Runs on port 3000 with HMR
- **API Proxy**: Routes `/api/*` to backend at `http://localhost:8000`
- **Path Aliases**: `@/*` resolves to `src/*` for clean imports
- **Build Output**: Builds to `../../backend/api/ui` for integrated deployment
- **Tailwind Integration**: Native Tailwind CSS 4 support with `@tailwindcss/vite`
- **React Plugin**: Fast Refresh and JSX transformation
- **TypeScript**: Full TypeScript support with type checking

### TypeScript Configuration

- **Strict Mode**: Full TypeScript strict mode enabled for maximum type safety
- **Path Mapping**: Absolute imports with `@/` prefix for better organization
- **Modern Target**: ES2022 for optimal performance and modern features
- **React 19**: Latest React types with new features support

## 🎨 UI Components & Design System

### Component Library

- **shadcn/ui**: High-quality, accessible React components built on Radix UI
- **Vercel AI Elements**: Pre-built AI components for chat interfaces, message handling, and streaming responses
- **ECharts & Recharts**: Comprehensive charting libraries for data visualization and interactive dashboards
- **Radix UI**: Comprehensive collection of unstyled, accessible primitives
- **Lucide React**: Beautiful, customizable SVG icon library (500+ icons)
- **Tabler Icons**: Additional icon set with 4000+ free SVG icons
- **Tailwind CSS 4**: Utility-first CSS framework with native Vite integration
- **Class Variance Authority**: Type-safe component variants and styling
- **Tailwind Merge**: Intelligent Tailwind class merging utility

### Theme System

- **Dark/Light Mode**: Built-in theme switching with `next-themes`
- **Responsive Design**: Mobile-first approach
- **Design Tokens**: Consistent spacing, colors, and typography

### Key Components

- **Layouts**: Dashboard with sidebar, default layout
- **Forms**: React Hook Form with Zod validation and input components
- **Data Tables**: TanStack Table with sorting, filtering, and pagination
- **Charts**: Recharts integration for data visualization and ECharts support
- **Notifications**: Sonner for beautiful toast notifications
- **Carousels**: Embla Carousel for responsive image/content carousels
- **Resizable Panels**: React Resizable Panels for flexible layouts
- **Command Palette**: CMDK for searchable command interfaces
- **Syntax Highlighting**: React Syntax Highlighter for code display
- **Motion**: Framer Motion for smooth animations and transitions
- **Drawers**: Vaul for mobile-friendly drawer components

## 🔐 Authentication & Authorization

### Auth Provider

The `AuthProvider` manages:
- User session state and JWT token handling
- Automatic token refresh with background workers
- Protected route access and role-based permissions
- **WebAuthn Integration**: Passwordless authentication support
- Multi-factor authentication capabilities

### WebAuthn Support

Modern passwordless authentication using:
- **@simplewebauthn/browser**: Client-side WebAuthn implementation
- Biometric authentication (fingerprint, face recognition)
- Hardware security keys (YubiKey, etc.)
- Enhanced security without passwords


## 🌐 API Integration

### Auto-Generated Client

The API client is automatically generated from the backend's OpenAPI specification:

```typescript
import { ApiClient } from '@/api'

const apiClient = new ApiClient({
  HEADERS: {
    Authorization: `Bearer ${accessToken}`
  }
})

// Type-safe API calls
const users = await apiClient.users.getUsersApiV1UsersGet()
```

### API Client Generation

When the backend API changes:

1. Ensure backend is running on `http://localhost:8000`
2. Run `pnpm run generate:api`
3. Updated TypeScript types and services are automatically generated

## 🏠 Feature Components

### Dashboard
- **Sidebar Navigation**: Role-based menu with icons
- **Responsive Layout**: Mobile-friendly sidebar collapse
- **Breadcrumb Navigation**: Context-aware navigation

### User Management
- **User List**: Paginated table with search and filters
- **User Profile**: Complete profile management with image upload
- **Role Assignment**: Assign roles to users within tenants

### Tenant Management
- **Tenant Search**: Smart search with autocomplete
- **Multi-tenancy**: Tenant-scoped data and permissions
- **Tenant Switching**: Easy switching between tenants

### AI Chat Interface
- **Real-time Streaming**: Live AI responses with typing indicators using AI SDK
- **Model Selection**: Choose from available AI models with dynamic switching
- **Chat History**: Persistent conversation history with local storage
- **Mobile Optimized**: Touch-friendly chat interface with responsive design
- **Token Management**: Built-in token counting and usage tracking
- **Markdown Support**: Rich text rendering with syntax highlighting
- **Streaming Responses**: Real-time response streaming with `use-stick-to-bottom`

### Advanced UI Features
- **XY Flow**: Interactive node-based diagrams and flowcharts
- **Data Visualization**: ECharts integration for complex charts and graphs
- **State Management**: Zustand for lightweight, scalable state management
- **URL State**: nuqs for type-safe URL state synchronization
- **OTP Input**: Secure one-time password input components
- **Unique IDs**: nanoid for generating unique identifiers

### Role & Permission Management
- **Dynamic Roles**: Create and edit roles with permissions
- **Permission Matrix**: Visual permission assignment
- **Role Hierarchy**: Support for role inheritance

## 🎨 Styling & Theming

### Tailwind CSS 4

- **Native Vite Integration**: Direct Vite plugin support with `@tailwindcss/vite`
- **Custom Configuration**: Extended theme with design tokens and custom utilities
- **Dark Mode**: Automatic dark/light mode switching with `next-themes`
- **Responsive Design**: Mobile-first breakpoints with advanced responsive utilities
- **Animation Support**: Built-in animations with `tw-animate-css` integration

### Component Styling

```typescript
// Example component with Tailwind classes and CVA variants
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

function Button({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean
  }) {
  const Comp = asChild ? Slot : "button"

  return (
    <Comp
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}
```

## 🧪 Development Workflow

### Code Quality & Linting

1. **Biome Integration**: Ultra-fast linting and formatting
   ```bash
   pnpm lint          # Check for linting issues
   pnpm lint:fix      # Auto-fix linting issues
   pnpm format        # Format code with Biome
   ```

2. **TypeScript**: Strict type checking with modern features
   ```bash
   pnpm type-check    # Run TypeScript compiler checks
   ```

### API-First Development

1. **Backend Changes**: Update backend API endpoints
2. **Generate Client**: Run `pnpm run generate:api`
3. **Type Safety**: TypeScript ensures type safety across the stack
4. **Frontend Updates**: Use updated types and services

### Component Development

1. **shadcn/ui**: Use existing components when possible
2. **Custom Components**: Build in `components/shared/` for reusability
3. **Feature Components**: Organize by feature in `components/features/`
4. **Type Safety**: Use TypeScript interfaces for all props
5. **Styling**: Use CVA for component variants and Tailwind for styling

### Form Handling

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'

const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email')
})

function MyForm() {
  const form = useForm({
    resolver: zodResolver(schema),
    defaultValues: { name: '', email: '' }
  })
  
  const onSubmit = (data) => {
    // Type-safe form data
    console.log(data) // { name: string, email: string }
  }
  
  return <Form {...form}>...</Form>
}
```

## 📦 Build & Deployment

### Development Build

```bash
pnpm dev                    # Hot reload development server
```

### Production Build

```bash
pnpm build                  # TypeScript compilation + Vite build
pnpm preview                # Preview production build locally
```

### Build Output

- **Target Directory**: `../../backend/api/ui`
- **Optimized Assets**: Minified JavaScript, CSS, and assets
- **Static Files**: Ready for serving from any web server

## 🔧 Troubleshooting

### Common Issues

1. **API Client Generation Fails**:
   - Ensure backend is running on port 8000
   - Check backend OpenAPI endpoint: `http://localhost:8000/openapi.json`

2. **TypeScript Errors**:
   - Run `pnpm run generate:api` after backend changes
   - Clear TypeScript cache: Delete `node_modules/.cache`

3. **Styling Issues**:
   - Check Tailwind configuration
   - Verify component imports from `@/components/ui`

4. **Cloudflare DNS**:
    - Tenant contains subdomain for example:  `test.demo.fsrapp.xyz` then clouldflare doesn't provide free ssl certificate.. [Read here](https://developers.cloudflare.com/ssl/edge-certificates/)

### Development Tips

- **Hot Reload**: Vite provides instant hot module replacement
- **Type Checking**: Use `tsc --noEmit` for type checking without building
- **Debugging**: React Developer Tools and browser DevTools
- **Performance**: Use React Profiler for performance optimization

## 🤝 Contributing

1. **Follow TypeScript**: All new code should be TypeScript
2. **Use shadcn/ui**: Prefer existing components over custom ones
3. **Responsive Design**: Ensure mobile compatibility
4. **Type Safety**: Maintain end-to-end type safety
5. **API Integration**: Regenerate API client after backend changes

---

This frontend application provides a solid foundation for building modern, type-safe React applications with comprehensive UI components and seamless backend integration.