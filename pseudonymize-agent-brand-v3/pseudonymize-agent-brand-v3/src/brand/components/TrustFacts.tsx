export type VerifiedTrustFact = { label: string; value: string; source?: string }
export function TrustFacts({ facts }: { facts: VerifiedTrustFact[] }) {
  if (!facts.length) return null
  return <dl className="pz-trust-facts">{facts.map((fact) => <div key={fact.label}><dt>{fact.label}</dt><dd>{fact.value}</dd></div>)}</dl>
}
