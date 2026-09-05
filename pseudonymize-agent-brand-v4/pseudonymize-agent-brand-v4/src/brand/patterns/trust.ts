import type { VerifiedTrustClaim } from '../security'

export function visibleTrustClaims(claims: VerifiedTrustClaim[]) {
  return claims.filter((claim) => Boolean(claim.source && claim.verifiedAt && claim.value))
}
