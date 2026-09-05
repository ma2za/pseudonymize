export const brandCopy = {
  tagline: 'Keep the context. Replace the identifiers.',
  positioning:
    'Pseudonymize sensitive identifiers before data reaches systems that do not need the originals, while preserving the surrounding context and structure the workflow still needs.',

  homepage: {
    eyebrow: 'PSEUDONYMIZATION INFRASTRUCTURE',
    h1: 'Pseudonymize sensitive data before it reaches systems that do not need the original identifiers.',
    lead: 'Replace personal identifiers across text, structured data and files while preserving the surrounding context your workflow depends on.',
    primaryCta: 'Pseudonymize data',
    secondaryCta: 'View documentation',
    inputs: {
      heading: 'One operation across the data you actually use.',
      text: 'Replace identifiers inside prose without flattening the text around them.',
      data: 'Pseudonymize identifier fields while keeping rows and schemas usable.',
      files: 'Process supported files without manually extracting their sensitive content first.',
    },
    proof: {
      heading: 'Replace the identifier. Keep everything around it.',
    },
    workflow: {
      heading: 'Pseudonymization belongs before unnecessary exposure.',
      steps: ['Detect identifiers', 'Replace them with pseudonyms', 'Continue the workflow'],
    },
    developers: {
      heading: 'Put it in the data path.',
      cta: 'Read the docs',
    },
    trust: {
      heading: 'Inspect the handling, not the adjectives.',
    },
    final: {
      h2: 'Keep the context. Replace the identifiers.',
      primaryCta: 'Pseudonymize data',
      secondaryCta: 'View documentation',
    },
  },

  product: {
    h1: 'One pseudonymization layer for text, structured data and files.',
    lead: 'Send supported content through one processing layer, replace detected identifiers with pseudonyms, and continue working with the surrounding context intact.',
    primaryCta: 'Pseudonymize data',
    secondaryCta: 'Read the docs',
    modelHeading: 'The context stays. The identifiers change.',
    reviewHeading: 'Review what needs attention.',
    integrationHeading: 'Integrate where the data moves.',
  },

  developers: {
    h1: 'Put pseudonymization in the path of sensitive data.',
    lead: 'Use the API or supported integration surface to replace identifiers before content reaches downstream systems that do not require the originals.',
    primaryCta: 'Read the docs',
    secondaryCta: 'Pseudonymize data',
    requestHeading: 'One real request. One real result.',
  },

  security: {
    h1: 'Security claims should be inspectable.',
    lead: 'This page documents how pseudonymize.io handles data and infrastructure. Every claim shown here must be backed by an internal source or public policy.',
  },

  pricing: {
    usageBasedH1: 'Pricing that follows actual usage.',
    note: 'Use this heading only when the real billing model is usage-based.',
  },

  docs: {
    h1: 'Documentation',
    lead: 'Integrate pseudonymization into your workflow, understand supported inputs, and handle processing results and errors.',
  },

  about: {
    h1: 'Sensitive data should not travel farther than it needs to.',
    lead: 'Many workflows need the information around an identifier without needing the identifier itself. pseudonymize.io exists to make that separation practical.',
  },

  app: {
    workspaceTitle: 'Pseudonymize',
    sourceTitle: 'Source',
    resultTitle: 'Result',
    textEmpty: 'Paste text containing identifiers you want to replace.',
    fileEmpty: 'Choose a supported file to process.',
    resultEmpty: 'The pseudonymized result will appear here.',
    processAction: 'Pseudonymize',
    copyResult: 'Copy result',
    downloadResult: 'Download result',
    viewMappings: 'View mappings',
    historyTitle: 'Processing history',
    historyEmpty: 'No processed items yet.',
    mappingsTitle: 'Mappings',
    mappingsLead: 'Inspect the relationship between original identifiers and their pseudonyms.',
    apiKeysTitle: 'API keys',
    apiKeysLead: 'Create and manage credentials used to access the pseudonymize.io API.',
    createApiKey: 'Create API key',
    revokeKey: 'Revoke key',
    settingsTitle: 'Settings',
  },

  auth: {
    signInH1: 'Sign in',
    signUpH1: 'Create your account',
    signUpLead: 'Start pseudonymizing supported data and configure integrations available to your workspace.',
  },

  system: {
    notFoundH1: 'Page not found',
    notFoundBody: 'The page you requested does not exist or has moved.',
    notFoundCta: 'Go to pseudonymize.io',
    genericErrorH1: 'Something failed',
  },

  labels: {
    original: 'Original',
    pseudonymized: 'Pseudonymized',
    sensitive: 'Sensitive identifier',
    detected: 'Detected identifier',
    reviewRequired: 'Review required',
    processing: 'Processing',
    failed: 'Failed',
    notProcessed: 'Not processed',
  },
} as const
