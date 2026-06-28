import type { DailyCompletions, Tier } from '../types'

export interface DailyTaskDef {
  id: string
  label: string
  tiers: Tier[]
  times: string[]
  kind: 'once' | 'slots'
}

export const DAILY_TASKS: DailyTaskDef[] = [
  { id: 'vitals', label: 'Daily vitals', tiers: ['green', 'yellow', 'red', 'black'], times: ['08:00'], kind: 'once' },
  { id: 'water', label: 'Water', tiers: ['green', 'yellow', 'red', 'black'], times: ['09:00', '11:00', '13:00', '15:00', '17:00', '19:00'], kind: 'slots' },
  { id: 'meds', label: 'Meds', tiers: ['green', 'yellow', 'red', 'black'], times: ['08:30'], kind: 'once' },
  { id: 'bathroom', label: 'Bathroom', tiers: ['green', 'yellow', 'red', 'black'], times: ['09:30', '14:00', '20:00'], kind: 'slots' },
  { id: 'teeth', label: 'Brush teeth', tiers: ['green', 'yellow', 'red'], times: ['09:00', '21:00'], kind: 'slots' },
  { id: 'face', label: 'Wash face', tiers: ['green', 'yellow', 'red'], times: ['09:15'], kind: 'once' },
  { id: 'meal_am', label: 'Morning food', tiers: ['green', 'yellow', 'red'], times: ['09:00'], kind: 'once' },
  { id: 'meal_mid', label: 'Midday food', tiers: ['green', 'yellow', 'red'], times: ['13:00'], kind: 'once' },
  { id: 'meal_pm', label: 'Evening food', tiers: ['green', 'yellow', 'red'], times: ['18:00'], kind: 'once' },
  { id: 'reset_mid', label: 'Midday reset', tiers: ['green', 'yellow'], times: ['13:00'], kind: 'once' },
  { id: 'reset_deep', label: 'Reset-deep before bed', tiers: ['green', 'yellow', 'red'], times: ['21:30'], kind: 'once' },
  { id: 'shutdown', label: 'Shutdown script', tiers: ['green', 'yellow', 'red', 'black'], times: ['22:00'], kind: 'once' },
]

function slotKey(task: DailyTaskDef, time: string): string {
  return task.kind === 'once' ? '*' : time
}

export function emptyDailyCompletions(date: string): DailyCompletions {
  return { date, done: {} }
}

export function ensureDailyCompletions(record: DailyCompletions | undefined, today: string): DailyCompletions {
  if (!record || record.date !== today) return emptyDailyCompletions(today)
  return record
}

export function isTaskDone(record: DailyCompletions, taskId: string, slot: string): boolean {
  const slots = record.done[taskId] ?? []
  return slots.includes(slot) || slots.includes('*')
}

export function markTaskDone(record: DailyCompletions, taskId: string, slot: string): DailyCompletions {
  const slots = new Set(record.done[taskId] ?? [])
  slots.add(slot)
  return {
    ...record,
    done: { ...record.done, [taskId]: [...slots].sort() },
  }
}

export function pendingTasksForTier(
  tier: Tier,
  record: DailyCompletions,
  now = new Date(),
): Array<DailyTaskDef & { slot: string; due: string }> {
  const hm = now.toTimeString().slice(0, 5)
  const out: Array<DailyTaskDef & { slot: string; due: string }> = []

  for (const task of DAILY_TASKS) {
    if (!task.tiers.includes(tier)) continue
    for (const time of task.times) {
      if (hm < time) continue
      const slot = slotKey(task, time)
      if (!isTaskDone(record, task.id, slot)) {
        out.push({ ...task, slot, due: time })
      }
    }
  }
  return out
}

export function mergeDailyCompletions(
  local: DailyCompletions | undefined,
  remote: DailyCompletions | undefined,
  today: string,
): DailyCompletions {
  const base = ensureDailyCompletions(local, today)
  if (!remote || remote.date !== today) return base
  const done = { ...base.done }
  for (const [taskId, slots] of Object.entries(remote.done ?? {})) {
    done[taskId] = [...new Set([...(done[taskId] ?? []), ...slots])].sort()
  }
  return { date: today, done }
}
