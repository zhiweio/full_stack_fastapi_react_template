# Full Stack FastAPI React Template - Frontend Rules

## Project Overview
This is a modern React 19 + TypeScript frontend application built with Vite 7, featuring AI chat capabilities, multi-tenant architecture, and WebAuthn authentication.

## Technology Stack
- **Framework**: React 19 with TypeScript (ES2022)
- **Build Tool**: Vite 7 with HMR and Fast Refresh
- **Styling**: Tailwind CSS 4 with shadcn/ui components
- **State Management**: Zustand for global state, nuqs for URL state
- **Forms**: React Hook Form with Zod validation
- **Authentication**: WebAuthn (passwordless), Magic Link, traditional login
- **AI Integration**: Vercel AI SDK with streaming responses
- **Data Visualization**: ECharts & Recharts
- **Code Quality**: Biome for linting/formatting, TypeScript strict mode

## Code Style & Standards

### TypeScript
- Use strict TypeScript with ES2022 target
- Prefer type inference over explicit typing when clear
- Use `interface` for object shapes, `type` for unions/intersections
- Always use proper typing for React components and props
- Utilize path mapping with `@/` prefix for imports

### React Patterns
- Use functional components with hooks exclusively
- Prefer composition over inheritance
- Use React.memo() for performance optimization when needed
- Implement proper error boundaries for robust UX
- Use Suspense for lazy loading and async operations

### Component Architecture
```
src/
├── components/
│   ├── ui/           # Reusable UI components (shadcn/ui)
│   ├── features/     # Feature-specific components
│   ├── shared/       # Shared business components
│   └── providers/    # Context providers
├── hooks/            # Custom React hooks
├── lib/              # Utility functions and configurations
├── stores/           # Zustand stores
└── types/            # TypeScript type definitions
```

### Styling Guidelines
- Use Tailwind CSS classes with semantic naming
- Implement dark mode support with `next-themes`
- Use `class-variance-authority` (CVA) for component variants
- Prefer `cn()` utility for conditional classes
- Follow mobile-first responsive design principles

### Component Development
- Use shadcn/ui as the base component library
- Implement proper accessibility (a11y) attributes
- Use Radix UI primitives for complex interactions
- Follow the compound component pattern for flexibility
- Implement proper loading and error states

### State Management
- Use Zustand for global application state
- Use `nuqs` for URL state synchronization
- Prefer local state (useState) for component-specific data
- Use React Query/SWR for server state management
- Implement proper state persistence when needed

### Form Handling
- Use React Hook Form with Zod schema validation
- Implement proper form accessibility and error handling
- Use controlled components for complex form logic
- Provide real-time validation feedback
- Handle form submission states (loading, success, error)

### Authentication & Security
- Implement WebAuthn for passwordless authentication
- Support multiple authentication methods (passkey, magic link, traditional)
- Use proper CSRF protection and secure headers
- Implement proper session management
- Follow security best practices for sensitive data

### AI Integration
- Use Vercel AI SDK for chat functionality
- Implement streaming responses with proper UI feedback
- Use `use-stick-to-bottom` for chat scroll behavior
- Handle AI model switching dynamically
- Implement proper token management and limits

### Performance Optimization
- Use React.lazy() for code splitting
- Implement proper image optimization
- Use virtualization for large lists (react-window)
- Optimize bundle size with tree shaking
- Implement proper caching strategies

### Code Quality Rules
- Follow Biome configuration for consistent formatting
- Use 2-space indentation, 80-character line width
- Prefer double quotes for strings and JSX attributes
- Use trailing commas in ES5 style
- Implement proper error handling with try-catch blocks
- Write descriptive commit messages following conventional commits

### Testing Guidelines
- Write unit tests for utility functions
- Use React Testing Library for component tests
- Implement integration tests for critical user flows
- Mock external dependencies properly
- Maintain good test coverage for business logic

### Import Organization
```typescript
// 1. Node modules
import React from "react"
import { useState } from "react"

// 2. Internal modules (absolute imports)
import { Button } from "@/components/ui/button"
import { useAuth } from "@/hooks/use-auth"

// 3. Relative imports
import "./component.css"
```

### Naming Conventions
- Use PascalCase for components and types
- Use camelCase for functions, variables, and props
- Use kebab-case for file names
- Use SCREAMING_SNAKE_CASE for constants
- Use descriptive names that explain intent

### Error Handling
- Implement proper error boundaries
- Use toast notifications for user feedback
- Log errors appropriately for debugging
- Provide fallback UI for failed states
- Handle network errors gracefully

### Accessibility
- Use semantic HTML elements
- Implement proper ARIA attributes
- Ensure keyboard navigation support
- Maintain proper color contrast ratios
- Test with screen readers

## Development Workflow
- Use `pnpm` as the package manager
- Run `pnpm lint` before commits
- Use `pnpm type-check` for TypeScript validation
- Follow feature branch workflow with descriptive names
- Write clear PR descriptions with context

## File Naming Patterns
- Components: `kebab-case.tsx` (e.g., `user-profile.tsx`)
- Hooks: `use-kebab-case.ts` (e.g., `use-auth.ts`)
- Utilities: `kebab-case.ts` (e.g., `format-date.ts`)
- Types: `kebab-case.types.ts` (e.g., `user.types.ts`)
- Stores: `kebab-case-store.ts` (e.g., `auth-store.ts`)

## Key Dependencies to Leverage
- UI: shadcn/ui, Radix UI, Lucide React, Tabler Icons
- Forms: React Hook Form, Zod
- State: Zustand, nuqs
- Animation: Framer Motion, Embla Carousel
- Charts: ECharts, Recharts
- AI: Vercel AI SDK, AI Elements
- Auth: SimpleWebAuthn
- Utils: clsx, tailwind-merge, nanoid, date-fns

Remember: Always prioritize user experience, accessibility, and maintainable code architecture.