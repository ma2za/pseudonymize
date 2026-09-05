type Status = 'idle' | 'processing' | 'pseudonymized' | 'review' | 'failed'
const label: Record<Status,string> = { idle:'Not processed', processing:'Processing', pseudonymized:'Pseudonymized', review:'Review required', failed:'Failed' }
export function StatusBadge({ status }: { status: Status }) {
  return <span className="pz-status" data-status={status}><span className="pz-status__dot" aria-hidden />{label[status]}</span>
}
