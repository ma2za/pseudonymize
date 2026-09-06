import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { BrandButton } from '@/brand/components';

export default function NotFound() {
  const t = useTranslations('NotFound');

  return (
    <div className="bg-[var(--pz-surface)] min-h-[100dvh] py-24 sm:py-32 border-t border-[var(--pz-border)] text-center flex items-center justify-center">
      <div className="pz-container px-4 sm:px-6 max-w-xl">
        <p className="text-sm font-semibold text-[var(--pz-cipher-strong)] uppercase tracking-widest mb-2">404 Error</p>
        <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-[var(--pz-text)] mb-6 leading-tight">
          {t('title')}
        </h1>
        <p className="text-lg text-[var(--pz-text-secondary)] mb-10 leading-relaxed">
          {t('description')}
        </p>
        <Link href="/" style={{ textDecoration: 'none' }} className="inline-block">
          <BrandButton>{t('cta')}</BrandButton>
        </Link>
      </div>
    </div>
  );
}
