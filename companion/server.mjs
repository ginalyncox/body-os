import { createServer } from 'node:http'
import { readFile } from 'node:fs/promises'
import { extname, join, normalize } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = fileURLToPath(new URL('./dist', import.meta.url))
const systemPrompt = `You are the BodyOS Incident Commander, a calm interface for a chronic-illness flare. Structure the user's report and select from user-authored runbooks. Never diagnose, infer a disease, prescribe, recommend medication changes, or replace emergency care. Use short concrete language for reduced working memory. Prefer stopping, supported positioning, lower stimulation, and the user's established clinician-approved plan. If the report suggests immediate danger, set emergency true and direct a US user to 911 or 988. Tiers describe capacity: green stable, yellow reduce load, red stop/conserve, black survival floor/outside help. Return only JSON: {"tier":"green|yellow|red|black","headline":"string","rationale":"string","immediateSafety":["string"],"steps":[{"title":"string","instruction":"string"}],"clinicianSummary":"string","postmortemPrompt":"string","emergency":false}. Use 2-5 steps. Report the user's words and severity without inventing causes.`
const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.json': 'application/json' }

function json(res, status, body) {
  res.writeHead(status, { 'content-type': 'application/json', 'cache-control': 'no-store' })
  res.end(JSON.stringify(body))
}

async function incident(req, res) {
  if (!process.env.OPENAI_API_KEY) return json(res, 503, { error: 'GPT-5.6 is not configured' })
  let raw = ''
  for await (const chunk of req) {
    raw += chunk
    if (raw.length > 20_000) return json(res, 413, { error: 'Request too large' })
  }
  const body = JSON.parse(raw || '{}')
  const description = String(body.description ?? '').trim().slice(0, 1200)
  const severity = Math.min(10, Math.max(1, Number(body.severity) || 1))
  if (description.length < 8) return json(res, 400, { error: 'Description is too short' })
  const response = await fetch('https://api.openai.com/v1/responses', { method: 'POST', headers: { authorization: `Bearer ${process.env.OPENAI_API_KEY}`, 'content-type': 'application/json' }, body: JSON.stringify({ model: 'gpt-5.6', reasoning: { effort: 'low' }, store: false, max_output_tokens: 1800, instructions: systemPrompt, input: `Current incident severity: ${severity}/10\nUser report: ${description}` }) })
  if (!response.ok) return json(res, 502, { error: 'Incident analysis unavailable' })
  const data = await response.json()
  const text = data.output_text ?? data.output?.flatMap((item) => item.content ?? []).find((item) => item.type === 'output_text')?.text
  const plan = JSON.parse(String(text).replace(/^```json\s*/i, '').replace(/\s*```$/, ''))
  if (!Array.isArray(plan.steps) || !plan.steps.length) throw new Error('Invalid plan')
  return json(res, 200, plan)
}

createServer(async (req, res) => {
  try {
    if (req.method === 'POST' && req.url === '/api/incident') return await incident(req, res)
    const requested = req.url === '/' ? 'index.html' : normalize(String(req.url).split('?')[0]).replace(/^[/\\]+/, '')
    const safePath = requested.includes('..') ? 'index.html' : requested
    let file
    try { file = await readFile(join(root, safePath)) } catch { file = await readFile(join(root, 'index.html')) }
    res.writeHead(200, { 'content-type': mime[extname(safePath)] ?? 'text/html; charset=utf-8' })
    res.end(file)
  } catch (error) {
    console.error(error)
    json(res, 500, { error: 'Incident analysis unavailable' })
  }
}).listen(process.env.PORT || 4173, () => console.log('BodyOS companion is ready'))
