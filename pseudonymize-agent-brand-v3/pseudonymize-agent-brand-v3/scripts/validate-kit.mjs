import fs from 'node:fs'
import path from 'node:path'
const root = path.resolve(process.argv[2] || '.')
const required = [
  'AGENTS.md','agent/specs/homepage.json','agent/specs/product.json','agent/specs/tokens.json',
  'src/brand/tokens.css','src/brand/components.css','src/brand/components/Logo.tsx',
  'public/brand/mark-dark.svg','public/brand/mark-light.svg','public/brand/lockup-dark.svg','public/brand/favicon.svg'
]
let ok = true
for (const rel of required) if (!fs.existsSync(path.join(root,rel))) { console.error('Missing', rel); ok=false }
for (const rel of fs.readdirSync(path.join(root,'agent/specs')).filter(x=>x.endsWith('.json'))) {
  JSON.parse(fs.readFileSync(path.join(root,'agent/specs',rel),'utf8'))
}
if (!ok) process.exit(1)
console.log('Kit validation passed.')
