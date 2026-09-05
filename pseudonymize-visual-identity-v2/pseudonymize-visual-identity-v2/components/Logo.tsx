type LogoProps = { compact?: boolean; className?: string }

export function Logo({ compact = false, className }: LogoProps) {
  return (
    <span className={className} aria-label="pseudonymize.io" style={{ display: "inline-flex", alignItems: "center", gap: 8 }}>
      <svg width="30" height="30" viewBox="0 0 128 128" aria-hidden="true">
        <rect width="128" height="128" rx="26" fill="#081016" />
        <path fill="#EEF5F7" fillRule="evenodd" d="M34 25h37c19.33 0 35 15.67 35 35S90.33 95 71 95H55v15H34V25Zm21 20v30h16c8.28 0 15-6.72 15-15s-6.72-15-15-15H55Z" />
        <path d="M86 24 41 102" stroke="#48D6B0" strokeWidth="9" strokeLinecap="round" />
      </svg>
      {!compact && <><strong style={{ letterSpacing: "-0.03em" }}>pseudonymize</strong><code style={{ color: "#48D6B0", marginLeft: -6, fontSize: 11 }}>.io</code></>}
    </span>
  )
}
