import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';

export default function Footer() {
  const t = useTranslations('Global');

  return (
    <footer className="bg-[var(--pz-canvas)] border-t border-[var(--pz-border)] transition-colors">
      <div className="pz-container overflow-hidden py-12 sm:py-16">
        <nav className="-mb-6 flex flex-wrap justify-center gap-x-12 gap-y-3 text-sm leading-6 font-medium" aria-label="Footer">
          <Link href="/blog" className="text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
            {t('blog')}
          </Link>
          <Link href="/privacy" className="text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
            {t('privacy')}
          </Link>
          <Link href="/terms" className="text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
            {t('terms')}
          </Link>
          <a href="https://github.com/ma2za/pseudonymize" target="_blank" rel="noopener noreferrer" className="text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
            {t('openSource')}
          </a>
        </nav>
        <p className="mt-10 text-center text-xs leading-5 text-[var(--pz-text-muted)] font-mono">
          {t('copyright')}
        </p>
      </div>
    </footer>
  );
}