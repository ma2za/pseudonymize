export type TrustClaimId =
  | 'retention'
  | 'processing_region'
  | 'encryption_at_rest'
  | 'encryption_in_transit'
  | 'data_residency'
  | 'deployment_mode'
  | 'subprocessors'
  | 'dpa'
  | 'soc2'
  | 'iso27001'

export type VerifiedTrustClaim = {
  id: TrustClaimId
  label: string
  value: string
  source: string // URL, internal config path, or evidence identifier. Required.
  verifiedAt: string // ISO date
}

// Deliberately empty. Populate only from product/repository facts.
export const verifiedTrustClaims: VerifiedTrustClaim[] = []
