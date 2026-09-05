import type { PropsWithChildren } from 'react'
export function PseudonymToken({ children }: PropsWithChildren) {
  return <code className="pz-token" data-pz-kind="pseudonym">{children}</code>
}
