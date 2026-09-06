'use client';

import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { authClient } from '@/lib/auth-client';
import LanguageSwitcher from './LanguageSwitcher';
import { ThemeToggle } from './ThemeToggle';
import { Logo, BrandButton } from '@/brand/components';
import { GithubIcon } from './GithubIcon';
import { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';

export default function Header() {
  const t = useTranslations('Global');
  const tHome = useTranslations('Home');
  const { data: session, isPending } = authClient.useSession();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Close mobile menu on route change implicitly via click handler
  const closeMenu = () => setMobileMenuOpen(false);

  // Lock body scroll when menu is open
  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
  }, [mobileMenuOpen]);

  return (
    <header className="bg-[var(--pz-surface)] border-b border-[var(--pz-border)] sticky top-0 z-50 transition-colors h-16 flex items-center">
      <nav className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8" aria-label="Global">
        <div className="flex items-center gap-6 lg:gap-10">
          <Link href="/" className="-m-1.5 p-1.5 flex items-center gap-2" onClick={closeMenu}>
            <Logo surface="light" width={150} />
          </Link>
          <div className="hidden lg:flex gap-x-6 items-center">
            <Link href="/docs" className="text-sm font-medium leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
              {t('docs')}
            </Link>
            <Link href="/pricing" className="text-sm font-medium leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
              {t('pricing')}
            </Link>
            <Link href="/security" className="text-sm font-medium leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
              {t('security')}
            </Link>
            <Link href="/benchmarks" className="text-sm font-medium leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
              {t('benchmarks')}
            </Link>
            <a href="https://github.com/ma2za/pseudonymize" target="_blank" rel="noopener noreferrer" className="flex items-center gap-1.5 text-sm font-medium leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
              <GithubIcon className="w-4 h-4" />
              <span>{t('github')}</span>
            </a>
          </div>
        </div>
        
        <div className="flex flex-1 justify-end items-center gap-2 sm:gap-4">
          <div className="hidden sm:block">
            <LanguageSwitcher />
          </div>
          <ThemeToggle />
          
          <div className="hidden sm:flex items-center gap-4">
            {!isPending && session ? (
              <>
                <Link href="/dashboard" className="text-sm font-medium leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
                  {t('dashboard')}
                </Link>
                <form action="/api/auth/signout" method="POST">
                  <button type="submit" className="rounded-md bg-[var(--pz-surface-inset)] border border-[var(--pz-border-strong)] px-3 py-1.5 text-sm font-medium text-[var(--pz-text)] shadow-sm hover:bg-[var(--pz-surface)] transition-colors">
                    {t('signOut')}
                  </button>
                </form>
              </>
            ) : !isPending ? (
              <>
                <Link href="/login" className="text-sm font-medium leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
                  {t('signIn')}
                </Link>
                <Link href="/signup" style={{ textDecoration: 'none' }}>
                  <BrandButton className="py-1.5 px-3 text-sm">{tHome('getStarted')}</BrandButton>
                </Link>
              </>
            ) : null}
          </div>

          <div className="flex lg:hidden">
            <button
              type="button"
              className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)]"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <span className="sr-only">Open main menu</span>
              {mobileMenuOpen ? (
                <X className="h-6 w-6" aria-hidden="true" />
              ) : (
                <Menu className="h-6 w-6" aria-hidden="true" />
              )}
            </button>
          </div>
        </div>
      </nav>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden fixed inset-0 z-40 top-16 bg-[var(--pz-canvas)] overflow-y-auto border-t border-[var(--pz-border)]">
          <div className="flex flex-col px-6 py-6 gap-y-4">
            <Link href="/docs" className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-[var(--pz-text)] hover:bg-[var(--pz-surface-inset)]" onClick={closeMenu}>
              {t('docs')}
            </Link>
            <Link href="/pricing" className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-[var(--pz-text)] hover:bg-[var(--pz-surface-inset)]" onClick={closeMenu}>
              {t('pricing')}
            </Link>
            <Link href="/security" className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-[var(--pz-text)] hover:bg-[var(--pz-surface-inset)]" onClick={closeMenu}>
              {t('security')}
            </Link>
            <Link href="/benchmarks" className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-[var(--pz-text)] hover:bg-[var(--pz-surface-inset)]" onClick={closeMenu}>
              {t('benchmarks')}
            </Link>
            <a href="https://github.com/ma2za/pseudonymize" target="_blank" rel="noopener noreferrer" className="-mx-3 flex items-center gap-2 rounded-lg px-3 py-2 text-base font-semibold leading-7 text-[var(--pz-text)] hover:bg-[var(--pz-surface-inset)]" onClick={closeMenu}>
              <GithubIcon className="w-5 h-5" />
              <span>{t('github')}</span>
            </a>
            
            <div className="py-4 border-y border-[var(--pz-border)] mt-4">
              <LanguageSwitcher />
            </div>

            <div className="pt-4 flex flex-col gap-4">
              {!isPending && session ? (
                <>
                  <Link href="/dashboard" className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-[var(--pz-text)] hover:bg-[var(--pz-surface-inset)]" onClick={closeMenu}>
                    {t('dashboard')}
                  </Link>
                  <form action="/api/auth/signout" method="POST" className="mt-2">
                    <button type="submit" className="w-full text-left -mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-[var(--pz-text)] hover:bg-[var(--pz-surface-inset)]">
                      {t('signOut')}
                    </button>
                  </form>
                </>
              ) : !isPending ? (
                <>
                  <Link href="/login" className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-[var(--pz-text)] hover:bg-[var(--pz-surface-inset)]" onClick={closeMenu}>
                    {t('signIn')}
                  </Link>
                  <Link href="/signup" style={{ textDecoration: 'none' }} onClick={closeMenu} className="mt-2 block w-full text-center">
                    <BrandButton className="w-full justify-center">{tHome('getStarted')}</BrandButton>
                  </Link>
                </>
              ) : null}
            </div>
          </div>
        </div>
      )}
    </header>
  );
}