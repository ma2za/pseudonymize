import Image from 'next/image'

type LogoProps = {
  surface?: 'dark' | 'light'
  compact?: boolean
  width?: number
  className?: string
  priority?: boolean
}

export function Logo({ surface = 'dark', compact = false, width, className, priority = false }: LogoProps) {
  const src = compact ? `/brand/mark-${surface}.svg` : `/brand/lockup-${surface}.svg`
  const w = width ?? (compact ? 32 : 164)
  const h = compact ? w : Math.round(w * 128 / 620)
  return <Image src={src} alt="pseudonymize.io" width={w} height={h} className={className} priority={priority} />
}
