import type { AppData } from '../types'

const SYNC_URL_KEY = 'body-os-robot-sync-url'

export function getRobotSyncUrl(): string {
  return localStorage.getItem(SYNC_URL_KEY) || 'http://127.0.0.1:8765/api/sync'
}

export function setRobotSyncUrl(url: string) {
  localStorage.setItem(SYNC_URL_KEY, url)
}

export async function pullFromRobot(baseUrl?: string): Promise<AppData> {
  const url = baseUrl || getRobotSyncUrl()
  const res = await fetch(url, { method: 'GET' })
  if (!res.ok) throw new Error(`Robot pull failed: ${res.status}`)
  const data = await res.json()
  return {
    version: data.version ?? 1,
    vitals: data.vitals ?? [],
    flares: data.flares ?? [],
    postmortems: data.postmortems ?? [],
  }
}

export async function pushToRobot(data: AppData, baseUrl?: string): Promise<{ merged: Record<string, number> }> {
  const url = baseUrl || getRobotSyncUrl()
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error(`Robot push failed: ${res.status}`)
  return res.json()
}

export async function checkRobotHealth(baseUrl?: string): Promise<boolean> {
  try {
    const url = (baseUrl || getRobotSyncUrl()).replace('/api/sync', '/api/health')
    const res = await fetch(url, { method: 'GET' })
    return res.ok
  } catch {
    return false
  }
}
