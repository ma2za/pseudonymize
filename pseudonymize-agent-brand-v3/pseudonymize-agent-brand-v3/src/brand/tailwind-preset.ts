import type { Config } from 'tailwindcss'

const preset: Partial<Config> = {
  theme: {
    extend: {
      colors: {
        pz: {
          canvas: 'var(--pz-canvas)', surface: 'var(--pz-surface)', raised: 'var(--pz-surface-raised)', inset: 'var(--pz-surface-inset)',
          border: 'var(--pz-border)', 'border-strong': 'var(--pz-border-strong)', text: 'var(--pz-text)', secondary: 'var(--pz-text-secondary)', muted: 'var(--pz-text-muted)',
          cipher: 'var(--pz-cipher)', 'cipher-hover': 'var(--pz-cipher-hover)', 'cipher-strong': 'var(--pz-cipher-strong)', 'cipher-soft': 'var(--pz-cipher-soft)',
          sensitive: 'var(--pz-sensitive)', 'sensitive-soft': 'var(--pz-sensitive-soft)', info: 'var(--pz-info)', danger: 'var(--pz-danger)', success: 'var(--pz-success)'
        }
      },
      fontFamily: { sans: ['var(--pz-font-sans)'], mono: ['var(--pz-font-mono)'] },
      borderRadius: { 'pz-sm': '6px', 'pz': '8px', 'pz-lg': '12px' },
      maxWidth: { 'pz': '1160px', 'pz-reading': '700px' },
      height: { 'pz-control': '40px' },
      minHeight: { 'pz-control': '40px' }
    }
  }
}
export default preset
