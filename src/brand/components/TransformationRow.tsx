import { PseudonymToken } from './PseudonymToken'

type Props = { label?: string; raw: string; pseudonym: string }
export function TransformationRow({ label, raw, pseudonym }: Props) {
  return (
    <div className="pz-map-row">
      {label && <span className="pz-map-row__label">{label}</span>}
      <span className="pz-map-row__raw">{raw}</span>
      <span aria-hidden className="pz-map-row__bond" />
      <PseudonymToken>{pseudonym}</PseudonymToken>
    </div>
  )
}
