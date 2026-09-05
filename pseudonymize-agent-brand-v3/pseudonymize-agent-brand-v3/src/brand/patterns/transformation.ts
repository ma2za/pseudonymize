export type TransformationPair = { entityType: string; original: string; pseudonym: string }

export const demoTransformation: TransformationPair[] = [
  { entityType: 'person', original: 'Alice Morgan', pseudonym: 'PERSON_01' },
  { entityType: 'email', original: 'alice@example.com', pseudonym: 'EMAIL_01' },
  { entityType: 'phone', original: '+49 151 555 0192', pseudonym: 'PHONE_01' },
]

// Synthetic demo data only. Never place real customer data into marketing examples.
