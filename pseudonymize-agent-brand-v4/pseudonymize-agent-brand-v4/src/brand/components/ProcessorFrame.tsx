import type { ReactNode } from 'react'
export function ProcessorFrame({ title = 'Pseudonymization preview', toolbar, children }: { title?: string; toolbar?: ReactNode; children: ReactNode }) {
  return <section className="pz-processor" aria-label={title}>
    <header className="pz-processor__header"><span>{title}</span>{toolbar}</header>
    <div className="pz-processor__body">{children}</div>
  </section>
}
