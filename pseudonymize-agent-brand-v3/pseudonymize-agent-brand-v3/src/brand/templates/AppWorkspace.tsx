import type { ReactNode } from 'react'
import { ProcessorFrame, StatusBadge } from '../components'

export function AppWorkspace({ source, result }: { source: ReactNode; result: ReactNode }) {
  return (
    <main className="pz-workspace">
      <header className="pz-workspace__toolbar"><span>Workspace</span><StatusBadge status="pseudonymized" /></header>
      <div className="pz-workspace__split">
        <ProcessorFrame title="Original">{source}</ProcessorFrame>
        <ProcessorFrame title="Pseudonymized">{result}</ProcessorFrame>
      </div>
    </main>
  )
}
