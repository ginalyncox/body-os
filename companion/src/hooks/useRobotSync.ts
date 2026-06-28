import { useCallback, useState } from 'react'
import type { AppData } from '../types'
import {
  checkRobotHealth,
  getRobotSyncUrl,
  pullFromRobot,
  pushToRobot,
  setRobotSyncUrl,
} from '../lib/robotSync'

export function useRobotSync(
  data: AppData,
  mergeRobotData: (incoming: AppData) => void,
) {
  const [syncUrl, setSyncUrlState] = useState(getRobotSyncUrl())
  const [status, setStatus] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const saveUrl = useCallback((url: string) => {
    setSyncUrlState(url)
    setRobotSyncUrl(url)
  }, [])

  const ping = useCallback(async () => {
    setLoading(true)
    setStatus(null)
    try {
      const ok = await checkRobotHealth(syncUrl)
      setStatus(ok ? 'Robot reachable' : 'Robot not responding')
    } catch {
      setStatus('Cannot reach robot — is python -m brain running?')
    } finally {
      setLoading(false)
    }
  }, [syncUrl])

  const pull = useCallback(async () => {
    setLoading(true)
    setStatus(null)
    try {
      const pulled = await pullFromRobot(syncUrl)
      mergeRobotData(pulled)
      const tasks = pulled.dailyCompletions?.done
        ? Object.keys(pulled.dailyCompletions.done).length
        : 0
      setStatus(`Pulled ${pulled.vitals.length} vitals, ${pulled.flares.length} flares, ${tasks} task marks`)
    } catch (e) {
      setStatus(e instanceof Error ? e.message : 'Pull failed')
    } finally {
      setLoading(false)
    }
  }, [syncUrl, mergeRobotData])

  const push = useCallback(async () => {
    setLoading(true)
    setStatus(null)
    try {
      const result = await pushToRobot(data, syncUrl)
      const m = result.merged
      setStatus(`Pushed — merged ${m.vitals ?? 0} vitals, ${m.flares ?? 0} flares, ${m.daily_completions ?? 0} task sync`)
    } catch (e) {
      setStatus(e instanceof Error ? e.message : 'Push failed')
    } finally {
      setLoading(false)
    }
  }, [syncUrl, data])

  return { syncUrl, saveUrl, ping, pull, push, status, loading }
}
