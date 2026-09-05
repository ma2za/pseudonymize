import { getTranslations, setRequestLocale } from 'next-intl/server';
import {Link} from '@/i18n/routing';
import { Shield } from 'lucide-react';

export default async function HomePage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Home');
  
  return (
    <div className="flex flex-col items-center justify-center p-4 sm:p-8 bg-gray-50 h-full mt-24">
      <article className="w-full max-w-2xl text-center space-y-8">
        <header className="flex flex-col items-center">
          <div className="flex justify-center mb-6">
            <Shield className="w-16 h-16 text-blue-600" aria-hidden="true" />
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            {t('title')}
          </h1>
        </header>
        <section>
          <p className="text-lg leading-8 text-gray-600">
            {t('description')}
          </p>
        </section>
        <nav aria-label="Primary action" className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-6">
          <Link
            href="/login"
            className="w-full sm:w-auto rounded-md bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
          >
            {t('getStarted')}
          </Link>
          <a href="https://github.com/ma2za/pseudonymize" target="_blank" rel="noopener noreferrer" className="text-sm font-semibold leading-6 text-gray-900 hover:text-blue-600">
            {t('viewOpenSource')} <span aria-hidden="true">→</span>
          </a>
        </nav>
      </article>
    </div>
  );
}