import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(process.argv[2] || process.cwd())
const allowedExt = new Set(['.ts','.tsx','.js','.jsx','.css','.mdx','.html'])
const ignoredDirs = new Set(['node_modules','.next','dist','build','.git','coverage','agent'])
const ignoredFiles = new Set(['AGENTS.md','README.md','brand-lint.mjs','security.ts'])
const riskyClaims = [
  /military[- ]grade/i, /unhackable/i, /zero[- ]risk/i, /bulletproof/i,
  /SOC\s*2/i, /ISO\s*27001/i, /HIPAA/i, /zero retention/i, /EU[- ]only/i,
  /end[- ]to[- ]end encryption/i, /GDPR compliant/i
]
const cliches = [/glassmorphism/i, /matrix rain/i, /ai sparkle/i, /hacker silhouette/i]
const suspiciousColors = ['#7c3aed','#8b5cf6','#a855f7','#06b6d4']
const findings = []

function walk(dir) {
  for (const name of fs.readdirSync(dir)) {
    if (ignoredDirs.has(name) || ignoredFiles.has(name)) continue
    const p = path.join(dir,name)
    const st = fs.statSync(p)
    if (st.isDirectory()) walk(p)
    else if (allowedExt.has(path.extname(name))) scan(p)
  }
}
function scan(file) {
  const s = fs.readFileSync(file,'utf8')
  for (const rx of riskyClaims) if (rx.test(s)) findings.push([file,'VERIFY_SECURITY_CLAIM',rx.toString()])
  for (const rx of cliches) if (rx.test(s)) findings.push([file,'VISUAL_CLICHE',rx.toString()])
  for (const c of suspiciousColors) if (s.toLowerCase().includes(c)) findings.push([file,'OFF_BRAND_COLOR',c])
}
walk(root)
if (findings.length) {
  console.error('\nBrand lint findings. These require review; they are not proof of a bug:')
  for (const [file,kind,detail] of findings) console.error(`- ${kind}: ${path.relative(root,file)} :: ${detail}`)
  process.exitCode = 1
} else console.log('Brand lint: no obvious drift detected.')
