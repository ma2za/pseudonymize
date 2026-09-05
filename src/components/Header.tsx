import { getTranslations } from 'next-intl/server';
import { Link } from '@/i18n/routing';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import LanguageSwitcher from './LanguageSwitcher';
import { ThemeToggle } from './ThemeToggle';
import { Logo, BrandButton } from '@/brand/components';

export default async function Header() {
  const t = await getTranslations('Global');
  const session = await auth.api.getSession({
    headers: await headers()
  });

  return (
    <header className="bg-[var(--pz-surface)] border-b border-[var(--pz-border)] sticky top-0 z-50 transition-colors">
      <nav className="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
        <div className="flex lg:flex-1">
          <Link href="/" className="-m-1.5 p-1.5 flex items-center gap-2">
            <Logo surface="light" width={180} />
          </Link>
        </div>
        <div className="flex gap-x-8 items-center">
          <Link href="/pricing" className="text-sm font-semibold leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
            {t('pricing')}
          </Link>
          <Link href="/blog" className="text-sm font-semibold leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
            {t('blog')}
          </Link>
          <a href="https://github.com/ma2za/pseudonymize" target="_blank" rel="noopener noreferrer" className="text-sm font-semibold leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors hidden sm:block">
            {t('openSource')}
          </a>
          <LanguageSwitcher />
          <ThemeToggle />
        </div>
        <div className="flex flex-1 justify-end items-center gap-4">
          {session ? (
            <>
              <Link href="/dashboard" className="text-sm font-semibold leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
                {t('dashboard')}
              </Link>
              <form action="/api/auth/signout" method="POST" className="hidden sm:block">
                <button type="submit" className="rounded-md bg-[var(--pz-surface-inset)] border border-[var(--pz-border-strong)] px-3 py-2 text-sm font-semibold text-[var(--pz-text)] shadow-sm hover:bg-[var(--pz-surface)] transition-colors">
                  {t('signOut')}
                </button>
              </form>
            </>
          ) : (
            <>
              <Link href="/login" className="text-sm font-semibold leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
                {t('signIn')} <span aria-hidden="true" className="hidden sm:inline">&rarr;</span>
              </Link>
              <Link href="/signup" style={{ textDecoration: 'none' }} className="hidden sm:block">
                <BrandButton className="py-2 px-3 text-sm">{t('signUp')}</BrandButton>
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}