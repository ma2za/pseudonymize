export const brandConfig = {
  name: 'pseudonymize.io',
  tagline: 'Keep the context. Replace the identifiers.',
  visualConcept: 'preserved-frame-mapped-identity',
  preferredMarketingTheme: 'dark',
  preferredDocsTheme: 'light',
  semanticRules: {
    cipher: 'Only pseudonymized/generated values and the primary action.',
    sensitive: 'Detected original identifiers that require attention. Never errors.',
    danger: 'Failures and destructive actions only.',
    mono: 'Machine-readable identifiers, code, hashes, entity labels and file metadata.',
  },
  logo: {
    dark: '/brand/lockup-dark.svg',
    light: '/brand/lockup-light.svg',
    compactDark: '/brand/mark-dark.svg',
    compactLight: '/brand/mark-light.svg',
    mono: '/brand/mark-mono.svg',
  }
} as const
