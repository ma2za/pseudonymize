import { getTranslations } from 'next-intl/server';
import { Link } from '@/i18n/routing';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import LanguageSwitcher from './LanguageSwitcher';
import Image from 'next/image';

export default async function Header() {
  const t = await getTranslations('Global');
  const session = await auth.api.getSession({
    headers: await headers()
  });

  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-50">
      <nav className="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
        <div className="flex lg:flex-1">
          <Link href="/" className="-m-1.5 p-1.5 flex items-center gap-2">
            <Image src="/lockup-dark.svg" alt="pseudonymize.io" width={180} height={40} className="h-8 w-auto" />
          </Link>
        </div>
        <div className="flex gap-x-8 items-center">
          <Link href="/pricing" className="text-sm font-semibold leading-6 text-gray-900 hover:text-blue-600">
            {t('pricing')}
          </Link>
          <Link href="/blog" className="text-sm font-semibold leading-6 text-gray-900 hover:text-blue-600">
            {t('blog')}
          </Link>
          <a href="https://github.com/ma2za/pseudonymize" target="_blank" rel="noopener noreferrer" className="text-sm font-semibold leading-6 text-gray-900 hover:text-blue-600 hidden sm:block">
            {t('openSource')}
          </a>
          <LanguageSwitcher />
        </div>
        <div className="flex flex-1 justify-end items-center gap-4">
          {session ? (
            <>
              <Link href="/dashboard" className="text-sm font-semibold leading-6 text-gray-900 hover:text-blue-600">
                {t('dashboard')}
              </Link>
              <form action="/api/auth/signout" method="POST" className="hidden sm:block">
                <button type="submit" className="rounded-md bg-gray-100 px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-200">
                  {t('signOut')}
                </button>
              </form>
            </>
          ) : (
            <>
              <Link href="/login" className="text-sm font-semibold leading-6 text-gray-900 hover:text-blue-600">
                {t('signIn')} <span aria-hidden="true" className="hidden sm:inline">&rarr;</span>
              </Link>
              <Link href="/signup" className="rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 hidden sm:block">
                {t('signUp')}
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}