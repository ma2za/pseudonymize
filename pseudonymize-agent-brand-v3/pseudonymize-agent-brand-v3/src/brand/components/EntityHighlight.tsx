import type { PropsWithChildren } from 'react'
export function EntityHighlight({ children }: PropsWithChildren) {
  return <mark className="pz-entity" data-pz-kind="sensitive">{children}</mark>
}
