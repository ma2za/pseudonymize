/* eslint-disable */
'use client';

import { useTheme } from 'next-themes';
import { Moon, Sun } from 'lucide-react';
import { useEffect, useState } from 'react';

export function ThemeToggle() {
  const [mounted, setMounted] = useState(false);
  const { resolvedTheme, setTheme } = useTheme();

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <div className="w-8 h-8" aria-hidden="true" />;
  }

  return (
    <button
      onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
      className="p-2 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors rounded-md hover:bg-[var(--pz-surface-inset)] focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--pz-cipher)]"
      aria-label="Toggle theme"
    >
      {resolvedTheme === 'dark' ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
    </button>
  );
}