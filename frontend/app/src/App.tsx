import { Navigate, Route, Routes } from "react-router"
import { AIChat } from "@/components/features/ai-chat/ai-chat"
import { Activation } from "@/components/features/auth/activation"
import { Login } from "@/components/features/auth/login"
import { MagicLinkLoginValidate } from "@/components/features/auth/magic-link-login-validate"
import { PasswordResetConfirmation } from "@/components/features/auth/password_reset_confirmation"
import { PasswordResetRequest } from "@/components/features/auth/password-reset-request"
import Register from "@/components/features/auth/register"
import { Dashboard } from "@/components/features/dashboard/dashboard"
import { Profile } from "@/components/features/profile/profile"
import { Roles } from "@/components/features/roles/roles"
import { Settings } from "@/components/features/settings/settings"
import { Tenants } from "@/components/features/tenant/tenant"
import { TenantSetting } from "@/components/features/tenant/tenant-setting"
import { Users } from "@/components/features/users/users"
import { DashboardLayout } from "@/components/layouts/dashboard-layout"
import { DefaultLayout } from "@/components/layouts/default-layout"
import { AIChatProvider } from "@/components/providers/ai-chat-provider"
import { RolesProvider } from "@/components/providers/roles-provider"
import { SettingsProvider } from "@/components/providers/settings-provider"
import { TenantsProvider } from "@/components/providers/tenant-provider"
import { UsersProvider } from "@/components/providers/users-provider"
import { useAuthContext } from "./components/providers/auth-provider"

function App() {
  const { user } = useAuthContext()
  return (
    <Routes>
      <Route element={<DefaultLayout />}>
        <Route index path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
        <Route path="forgot-password" element={<PasswordResetRequest />} />
        <Route
          path="password_reset_confirmation"
          element={<PasswordResetConfirmation />}
        />
        <Route path="activation" element={<Activation />} />
        <Route path="magic_link_login" element={<MagicLinkLoginValidate />} />
      </Route>

      <Route element={<DashboardLayout />}>
        <Route index path="dashboard" element={<Dashboard />} />
        <Route
          path="users"
          element={
            <UsersProvider>
              <Users />
            </UsersProvider>
          }
        />
        <Route
          path="roles"
          element={
            <RolesProvider>
              <Roles />
            </RolesProvider>
          }
        />
        {!user?.tenant_id && (
          <Route
            path="tenants"
            element={
              <TenantsProvider>
                <Tenants />
              </TenantsProvider>
            }
          />
        )}

        <Route
          path="settings"
          element={
            <SettingsProvider>
              <Settings />
            </SettingsProvider>
          }
        />

        <Route
          path="settings/tenant"
          element={
            <SettingsProvider>
              <TenantsProvider>
                <TenantSetting />
              </TenantsProvider>
            </SettingsProvider>
          }
        />

        <Route path="profile" element={<Profile />} />
        <Route
          path="ai"
          element={
            <AIChatProvider>
              <AIChat />
            </AIChatProvider>
          }
        />

        <Route path="*" element={<Navigate to="/dashboard" />} />
      </Route>
    </Routes>
  )
}

export default App
