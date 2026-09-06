import { getTranslations } from 'next-intl/server';
import { Link } from '@/i18n/routing';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import LanguageSwitcher from './LanguageSwitcher';
import { ThemeToggle } from './ThemeToggle';
import { Logo, BrandButton } from '@/brand/components';
import { GithubIcon } from './GithubIcon';

export default async function Header() {
  const t = await getTranslations('Global');
  const tHome = await getTranslations('Home');
  const session = await auth.api.getSession({
    headers: await headers()
  });

  return (
    <header className="bg-[var(--pz-surface)] border-b border-[var(--pz-border)] sticky top-0 z-50 transition-colors h-16 flex items-center">
      <nav className="mx-auto flex w-full max-w-7xl items-center justify-between px-6 lg:px-8" aria-label="Global">
        <div className="flex items-center gap-10">
          <Link href="/" className="-m-1.5 p-1.5 flex items-center gap-2">
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
        
        <div className="flex flex-1 justify-end items-center gap-4">
          <LanguageSwitcher />
          <ThemeToggle />
          {session ? (
            <>
              <Link href="/dashboard" className="text-sm font-medium leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
                {t('dashboard')}
              </Link>
              <form action="/api/auth/signout" method="POST" className="hidden sm:block">
                <button type="submit" className="rounded-md bg-[var(--pz-surface-inset)] border border-[var(--pz-border-strong)] px-3 py-1.5 text-sm font-medium text-[var(--pz-text)] shadow-sm hover:bg-[var(--pz-surface)] transition-colors">
                  {t('signOut')}
                </button>
              </form>
            </>
          ) : (
            <>
              <Link href="/login" className="text-sm font-medium leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
                {t('signIn')}
              </Link>
              <Link href="/signup" style={{ textDecoration: 'none' }} className="hidden sm:block">
                <BrandButton className="py-1.5 px-3 text-sm">{tHome('getStarted')}</BrandButton>
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}