import type { ButtonHTMLAttributes, PropsWithChildren } from 'react'

type Props = PropsWithChildren<ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' | 'ghost' }>

export function BrandButton({ variant = 'primary', className = '', children, ...props }: Props) {
  const variantClass = {
    primary: 'pz-btn pz-btn--primary',
    secondary: 'pz-btn pz-btn--secondary',
    ghost: 'pz-btn pz-btn--ghost',
  }[variant]
  return <button className={`${variantClass} ${className}`.trim()} {...props}>{children}</button>
}
