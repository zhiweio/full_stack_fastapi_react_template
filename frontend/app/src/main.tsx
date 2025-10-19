import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import App from "./App.tsx"
import { ThemeProvider } from "./components/providers/theme-provider.tsx"
import "./index.css"
import { BrowserRouter } from "react-router"
import { AppConfigProvider } from "@/components/providers/app-config-provider.tsx"
import { AuthProvider } from "./components/providers/auth-provider.tsx"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter basename="/">
      <AuthProvider>
        <AppConfigProvider>
          <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            <App />
          </ThemeProvider>
        </AppConfigProvider>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
)
