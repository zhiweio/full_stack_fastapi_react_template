import { useEffect, useState } from "react"
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import type { DashboardMetricsDto } from "@/api"
import { useAuthContext } from "@/components/providers/auth-provider"
import { Loading } from "@/components/shared/loading"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { getApiClient } from "@/lib/utils"
import { AllCards } from "./all-cards"

export function Dashboard() {
  const [filter, setFilter] = useState<"today" | "this_week" | "last_3_months">(
    "this_week"
  )
  const [data, setData] = useState<DashboardMetricsDto | null>(null)

  const { accessToken } = useAuthContext()
  useEffect(() => {
    async function fetchData() {
      try {
        const metrics = await getApiClient(
          accessToken
        ).dashboard.getDashboardMetricsApiV1DashboardGet({ filter })
        setData(metrics)
      } catch (error) {
        if (error instanceof Error) {
          console.error("Error fetching dashboard metrics:", error.cause)
          // window.location.reload();
          // await refreshCurrentUser();
        }
      }
    }
    fetchData()
  }, [filter, accessToken])

  return (
    <div>
      <div className="@container/main flex flex-1 flex-col gap-2 pb-10">
        <AllCards />
      </div>
      <Card>
        <CardHeader>
          <CardTitle>User Growth ({filter.replace("_", " ")})</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2 mb-4">
            <Button
              variant={filter === "today" ? "default" : "outline"}
              onClick={() => setFilter("today")}
            >
              Today
            </Button>
            <Button
              variant={filter === "this_week" ? "default" : "outline"}
              onClick={() => setFilter("this_week")}
            >
              This Week
            </Button>
            <Button
              variant={filter === "last_3_months" ? "default" : "outline"}
              onClick={() => setFilter("last_3_months")}
            >
              Last 3 Months
            </Button>
          </div>

          {data ? (
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data.timeseries}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="_id" />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="count"
                    stroke="#4f46e5" // Indigo-600
                    strokeWidth={2}
                    dot={{ r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
              <div className="mt-4 flex justify-between text-sm text-muted-foreground">
                <span>Total Users: {data.total_users}</span>
                <span>New: {data.joined_users}</span>
              </div>
            </div>
          ) : (
            <Loading variant="dots" size="md" text="Fetching Metrics..." />
          )}
        </CardContent>
      </Card>
    </div>
  )
}
