import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';

export default function Footer() {
  const t = useTranslations('Global');

  return (
    <footer className="bg-white border-t border-gray-100">
      <div className="mx-auto max-w-7xl overflow-hidden px-6 py-12 sm:py-16 lg:px-8">
        <nav className="-mb-6 flex flex-wrap justify-center gap-x-12 gap-y-3 text-sm leading-6" aria-label="Footer">
          <Link href="/blog" className="text-gray-600 hover:text-gray-900">
            {t('blog')}
          </Link>
          <Link href="/privacy" className="text-gray-600 hover:text-gray-900">
            {t('privacy')}
          </Link>
          <Link href="/terms" className="text-gray-600 hover:text-gray-900">
            {t('terms')}
          </Link>
          <a href="https://github.com/ma2za/pseudonymize" target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-gray-900">
            {t('openSource')}
          </a>
        </nav>
        <p className="mt-10 text-center text-xs leading-5 text-gray-500">
          {t('copyright')}
        </p>
      </div>
    </footer>
  );
}