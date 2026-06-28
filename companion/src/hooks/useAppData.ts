import { useCallback, useEffect, useState } from 'react'
import type { AppData, DailyVitals, FlareLog, Postmortem, Tier } from '../types'

const STORAGE_KEY = 'body-os-data'
const DATA_VERSION = 1

const emptyData = (): AppData => ({
  vitals: [],
  flares: [],
  postmortems: [],
  version: DATA_VERSION,
})

function normalizeData(value: unknown): AppData {
  const parsed = value && typeof value === 'object' ? value : {}
  const data = { ...emptyData(), ...parsed } as AppData

  return {
    ...data,
    vitals: Array.isArray(data.vitals) ? data.vitals : [],
    flares: Array.isArray(data.flares) ? data.flares : [],
    postmortems: Array.isArray(data.postmortems) ? data.postmortems : [],
    version: typeof data.version === 'number' ? data.version : DATA_VERSION,
  }
}

function loadData(): AppData {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return emptyData()
    return normalizeData(JSON.parse(raw))
  } catch {
    return emptyData()
  }
}

function saveData(data: AppData) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
}

export function useAppData() {
  const [data, setData] = useState<AppData>(loadData)

  useEffect(() => {
    saveData(data)
  }, [data])

  const addVitals = useCallback((vitals: Omit<DailyVitals, 'id' | 'createdAt'>) => {
    const entry: DailyVitals = {
      ...vitals,
      id: crypto.randomUUID(),
      createdAt: new Date().toISOString(),
    }
    setData((prev) => ({
      ...prev,
      vitals: [entry, ...prev.vitals.filter((v) => v.date !== vitals.date)],
    }))
    return entry
  }, [])

  const addFlare = useCallback((flare: Omit<FlareLog, 'id' | 'createdAt'>) => {
    const entry: FlareLog = {
      ...flare,
      id: crypto.randomUUID(),
      createdAt: new Date().toISOString(),
    }
    setData((prev) => ({ ...prev, flares: [entry, ...prev.flares] }))
    return entry
  }, [])

  const addPostmortem = useCallback((pm: Omit<Postmortem, 'id' | 'createdAt'>) => {
    const entry: Postmortem = {
      ...pm,
      id: crypto.randomUUID(),
      createdAt: new Date().toISOString(),
    }
    setData((prev) => ({ ...prev, postmortems: [entry, ...prev.postmortems] }))
    return entry
  }, [])

  const exportData = useCallback(() => {
    return JSON.stringify(data, null, 2)
  }, [data])

  const importData = useCallback((json: string) => {
    setData(normalizeData(JSON.parse(json)))
  }, [])

  const clearData = useCallback(() => {
    if (confirm('Delete all local data? This cannot be undone.')) {
      setData(emptyData())
    }
  }, [])

  return { data, addVitals, addFlare, addPostmortem, exportData, importData, clearData }
}

export function todayISO(): string {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export function suggestTier(vitals: Partial<DailyVitals>): Tier | null {
  if (!vitals.morningPain && vitals.morningPain !== 0) return null

  const pain = vitals.morningPain ?? 0
  const energy = vitals.morningEnergy ?? 5
  const sleep = vitals.sleepHours ?? 7
  const autonomic = vitals.autonomicState

  if (pain >= 9 || (autonomic === 'Hijacked' && pain >= 7)) return 'black'
  if (pain >= 7 || energy <= 3 || autonomic === 'Hijacked' || autonomic === 'Activated') return 'red'
  if (pain >= 4 || energy <= 5 || sleep < 6 || autonomic === 'Edgy') return 'yellow'
  if (pain <= 3 && energy >= 6 && sleep >= 6 && autonomic === 'Calm') return 'green'
  return 'yellow'
}

export function weekStats(vitals: DailyVitals[]) {
  const now = new Date()
  const weekAgo = new Date(now)
  weekAgo.setDate(weekAgo.getDate() - 7)

  const recent = vitals.filter((v) => new Date(v.date) >= weekAgo)
  const greenYellow = recent.filter((v) => v.tier === 'green' || v.tier === 'yellow').length
  const redBlack = recent.filter((v) => v.tier === 'red' || v.tier === 'black')

  return {
    daysLogged: recent.length,
    greenYellowDays: greenYellow,
    sloGreenYellow: greenYellow >= 5,
    redBlackDays: redBlack,
    recentVitals: recent,
  }
}

export function weekFlareStats(flares: FlareLog[]) {
  const now = new Date()
  const weekAgo = new Date(now)
  weekAgo.setDate(weekAgo.getDate() - 7)
  return flares.filter((f) => new Date(f.time) >= weekAgo && f.severity >= 6)
}
