import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Link } from '@/i18n/routing';
import { BrandButton, EntityHighlight, ProcessorFrame, PseudonymToken, TransformationRow } from '@/brand/components';
import type { Metadata } from 'next';
import { routing } from '@/i18n/routing';

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({locale, namespace: 'Product'});
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';

  const alternates: Record<string, string> = {
    'x-default': `${baseUrl}/product`,
  };
  routing.locales.forEach((l) => {
      alternates[l] = `${baseUrl}/${l}/product`;
  });

  return {
    title: `${t('title')} | pseudonymize.io`,
    description: t('description'),
    alternates: {
      canonical: `${baseUrl}/${locale}/product`,
      languages: alternates,
    },
  };
}

export default async function ProductPage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Product');

  return (
    <div className="pz-appbody">
      <section className="pz-home-hero">
        <div className="pz-home-hero__copy">
          <h1>{t('title')}</h1>
          <p className="pz-lead">{t('description')}</p>
          <div className="pz-actions">
            <Link href="/login" style={{ textDecoration: 'none' }}>
              <BrandButton>{t('primaryCta')}</BrandButton>
            </Link>
            <Link href="/docs" style={{ textDecoration: 'none' }}>
              <BrandButton variant="secondary">{t('secondaryCta')}</BrandButton>
            </Link>
          </div>
        </div>
        <ProcessorFrame>
          <p className="pz-sample-line">Extract data from <EntityHighlight>report.pdf</EntityHighlight>.</p>
          <TransformationRow label="File" raw="report.pdf" pseudonym="safe/report.pdf" />
          <p className="pz-sample-line">Extract data from <PseudonymToken>safe/report.pdf</PseudonymToken>.</p>
        </ProcessorFrame>
      </section>

      <section className="py-24 border-t border-[var(--pz-border)]">
        <div className="pz-container">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-[var(--pz-surface)] border border-[var(--pz-border-strong)] rounded-xl p-8">
              <div className="text-[var(--pz-cipher)] font-mono text-xs font-semibold mb-6">01 / TEXT</div>
              <h3 className="text-xl font-semibold text-[var(--pz-text)] mb-3">{t('textHeading')}</h3>
              <p className="text-[var(--pz-text-secondary)]">{t('textCopy')}</p>
            </div>
            <div className="bg-[var(--pz-surface)] border border-[var(--pz-border-strong)] rounded-xl p-8">
              <div className="text-[var(--pz-cipher)] font-mono text-xs font-semibold mb-6">02 / TABLES</div>
              <h3 className="text-xl font-semibold text-[var(--pz-text)] mb-3">{t('dataHeading')}</h3>
              <p className="text-[var(--pz-text-secondary)]">{t('dataCopy')}</p>
            </div>
            <div className="bg-[var(--pz-surface)] border border-[var(--pz-border-strong)] rounded-xl p-8">
              <div className="text-[var(--pz-cipher)] font-mono text-xs font-semibold mb-6">03 / FILES</div>
              <h3 className="text-xl font-semibold text-[var(--pz-text)] mb-3">{t('filesHeading')}</h3>
              <p className="text-[var(--pz-text-secondary)]">{t('filesCopy')}</p>
            </div>
          </div>
        </div>
      </section>

      <section className="py-32 bg-[var(--pz-ink)] text-white text-center">
        <div className="pz-container">
          <h2 className="text-3xl sm:text-5xl font-bold mb-10 leading-tight">
            {t('modelHeading')}
          </h2>
          <div className="max-w-2xl mx-auto border border-[#172630] rounded-xl overflow-hidden shadow-2xl">
            <div className="bg-[#121F29] p-8 border-b border-[#172630]">
              <h4 className="text-left text-[#A6B5BD] text-xs font-mono mb-4 uppercase tracking-widest">Original</h4>
              <div className="text-left font-mono text-sm leading-relaxed text-[#EEF5F7]">
                Patient <EntityHighlight>John Doe</EntityHighlight> was admitted to <EntityHighlight>Mercy Hospital</EntityHighlight> on <EntityHighlight>10/12/2026</EntityHighlight>.
              </div>
            </div>
            <div className="bg-[#050A0F] p-8">
              <h4 className="text-left text-[#A6B5BD] text-xs font-mono mb-4 uppercase tracking-widest">Pseudonymized Output</h4>
              <div className="text-left font-mono text-sm leading-relaxed text-[#EEF5F7]">
                Patient <PseudonymToken>PERSON_01</PseudonymToken> was admitted to <PseudonymToken>ORG_01</PseudonymToken> on <PseudonymToken>DATE_01</PseudonymToken>.
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}