import type { Metadata } from 'next'
export const pseudonymizeMetadata: Metadata = {
  title: { default: 'pseudonymize.io', template: '%s · pseudonymize.io' },
  description: 'Pseudonymize sensitive identifiers across text, structured data and files while preserving useful context.',
  icons: { icon: '/brand/favicon.svg' },
  openGraph: { type: 'website', title: 'pseudonymize.io', description: 'Keep the context. Replace the identifiers.' },
}
