export type Tier = 'green' | 'yellow' | 'red' | 'black'

export type AutonomicState = 'Calm' | 'Edgy' | 'Activated' | 'Hijacked'

export type PrimarySymptom =
  | 'Burning'
  | 'Itch'
  | 'Autonomic spike'
  | 'Brain fog'
  | 'Pain'
  | 'Hijack-feeling'
  | 'Numbness'
  | 'GI'
  | 'Insomnia'

export type BodyRegion =
  | 'Hands'
  | 'Feet'
  | 'Face'
  | 'Whole body'
  | 'Gut'
  | 'Legs'
  | 'Chest'
  | 'Head'

export type SuspectedTrigger =
  | 'Heat'
  | 'Cold'
  | 'Standing'
  | 'Food'
  | 'Screen'
  | 'Stress'
  | 'Sleep debt'
  | 'Hormonal'
  | 'Sensory load'
  | 'Unknown'

export type ScriptId = 'reset-60s' | 'reset-5min' | 'reset-deep' | 'shutdown' | 'none'

export interface DailyVitals {
  id: string
  date: string
  tier: Tier
  sleepHours: number
  sleepQuality: number
  morningPain: number
  morningEnergy: number
  autonomicState: AutonomicState
  cycleDay?: number
  notable?: string
  createdAt: string
}

export interface FlareLog {
  id: string
  summary: string
  time: string
  severity: number
  primarySymptom: PrimarySymptom
  bodyRegions: BodyRegion[]
  suspectedTriggers: SuspectedTrigger[]
  doingWhat?: string
  scriptRun: ScriptId
  timeToRecover?: string
  hoursSlept?: number
  lastMealHoursAgo?: number
  notes?: string
  createdAt: string
}

export interface Postmortem {
  id: string
  date: string
  tierReached: 'red' | 'black'
  peakSeverity: number
  duration?: string
  timeline: string
  whatHappened: string
  triggers: string
  whatWorked: string
  whatDidntWork: string
  pastSelfActions: string
  systemChanges: string
  sloImpact: string
  futureNote: string
  createdAt: string
}

export interface AppData {
  vitals: DailyVitals[]
  flares: FlareLog[]
  postmortems: Postmortem[]
  version: number
}

export interface GuidedStep {
  text: string
  durationSeconds?: number
}

export interface GuidedFlow {
  id: string
  title: string
  subtitle: string
  type: 'script' | 'runbook'
  trigger: string
  steps: GuidedStep[]
  successCriteria: string[]
  doNot: string[]
  fallback?: string
}

export interface ProtocolContent {
  tier: Tier
  title: string
  tagline: string
  entryCriteria: string[]
  allowed: string[]
  forbidden: string[]
  minimums: string[]
  exitUp?: string
  exitDown?: string
  notes: string
}

export interface KnownTrigger {
  name: string
  status: 'Confirmed' | 'Suspect' | 'Cleared'
  category: string
  severity: string
  mechanism: string
  mitigation: string
}
