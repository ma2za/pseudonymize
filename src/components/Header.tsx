import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Shield } from 'lucide-react';

export default function Header() {
  const t = useTranslations('Global');

  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-50">
      <nav className="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
        <div className="flex lg:flex-1">
          <Link href="/" className="-m-1.5 p-1.5 flex items-center gap-2">
            <Shield className="h-8 w-auto text-blue-600" />
            <span className="font-bold text-gray-900 text-xl tracking-tight">pseudonymize.io</span>
          </Link>
        </div>
        <div className="flex gap-x-8">
          <Link href="/blog" className="text-sm font-semibold leading-6 text-gray-900 hover:text-blue-600">
            {t('blog')}
          </Link>
          <a href="https://github.com/ma2za/pseudonymize" target="_blank" rel="noopener noreferrer" className="text-sm font-semibold leading-6 text-gray-900 hover:text-blue-600 hidden sm:block">
            {t('openSource')}
          </a>
        </div>
        <div className="flex flex-1 justify-end items-center gap-4">
          <Link href="/login" className="text-sm font-semibold leading-6 text-gray-900 hover:text-blue-600">
            {t('signIn')} <span aria-hidden="true" className="hidden sm:inline">&rarr;</span>
          </Link>
          <Link href="/signup" className="rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 hidden sm:block">
            {t('signUp')}
          </Link>
        </div>
      </nav>
    </header>
  );
}