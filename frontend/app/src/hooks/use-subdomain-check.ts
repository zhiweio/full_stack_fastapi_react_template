import { useEffect, useState } from "react"
import { ApiError, type SubdomainAvailabilityDto } from "@/api"
import { useAppConfig } from "@/components/providers/app-config-provider"
import { getApiClient } from "@/lib/utils"
import { useDebounce } from "./use-debounce"

export function useSubdomainCheck() {
  const { host_main_domain } = useAppConfig()
  const [subdomain, setSubdomain] = useState("")
  const debouncedText = useDebounce(subdomain, 800) // 800ms debounce
  const [subdomainAvailability, setSubdomainAvailability] =
    useState<SubdomainAvailabilityDto | null>(null)
  const [isChecking, setIsChecking] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function checkSubdomainAvailability() {
    const apiClient = getApiClient()
    try {
      setIsChecking(true)
      const response =
        await apiClient.tenants.checkSubdomainAvailabilityApiV1TenantsCheckSubdomainSubdomainGet(
          {
            subdomain: `${debouncedText}.${host_main_domain}`,
          }
        )
      setSubdomainAvailability(response)
      setError(null)
    } catch (error) {
      console.error("Error checking subdomain availability:", error)
      if (error instanceof ApiError) {
        setError(
          error.body?.detail ||
            "Failed to check subdomain availability. Please try again."
        )
      } else {
        setError("Failed to check subdomain availability. Please try again.")
      }
      setSubdomainAvailability(null)
    } finally {
      setIsChecking(false)
    }
  }
  useEffect(() => {
    if (debouncedText) {
      checkSubdomainAvailability()
    } else {
      setSubdomainAvailability(null)
      setError(null)
    }
  }, [debouncedText])

  return { setSubdomain, subdomainAvailability, isChecking, error }
}
