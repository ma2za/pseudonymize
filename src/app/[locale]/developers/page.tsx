/* eslint-disable react/no-unescaped-entities */
import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Link } from '@/i18n/routing';
import { BrandButton } from '@/brand/components';
import type { Metadata } from 'next';
import { routing } from '@/i18n/routing';

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({locale, namespace: 'Developers'});
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';

  const alternates: Record<string, string> = {
    'x-default': `${baseUrl}/developers`,
  };
  routing.locales.forEach((l) => {
      alternates[l] = `${baseUrl}/${l}/developers`;
  });

  const title = t('title');
  const description = t('description');

  return {
    title,
    description,
    alternates: {
      canonical: `${baseUrl}/${locale}/developers`,
      languages: alternates,
    },
    openGraph: {
      title,
      description,
      url: `${baseUrl}/${locale}/developers`,
      type: 'website',
      siteName: 'pseudonymize.io',
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
    }
  };
}

export default async function DevelopersPage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Developers');

  return (
    <div className="pz-appbody">
      {/* Hero Section */}
      <section className="py-24 sm:py-32">
        <div className="pz-container px-4 sm:px-6 max-w-4xl">
          <h1 className="text-4xl sm:text-6xl font-bold tracking-tight text-[var(--pz-text)] mb-6 leading-tight">
            {t('title')}
          </h1>
          <p className="text-xl text-[var(--pz-text-secondary)] mb-10 max-w-2xl leading-relaxed">
            {t('description')}
          </p>
          <div className="pz-actions">
            <Link href="/docs" style={{ textDecoration: 'none' }}>
              <BrandButton>{t('primaryCta')}</BrandButton>
            </Link>
            <Link href="/login" style={{ textDecoration: 'none' }}>
              <BrandButton variant="secondary">{t('secondaryCta')}</BrandButton>
            </Link>
          </div>
        </div>
      </section>

      {/* Terminal Block */}
      <section className="py-20 border-t border-[var(--pz-border)] bg-[var(--pz-surface)]">
        <div className="pz-container px-4 sm:px-6 grid md:grid-cols-2 gap-16 items-center">
          <div>
            <h2 className="pz-section-title mb-4">{t('requestHeading')}</h2>
            <p className="pz-subtitle">{t('description')}</p>
          </div>
          <div className="bg-[#050A0F] border border-[#172630] rounded-xl p-6 font-mono text-xs sm:text-sm text-[#758690] overflow-x-auto shadow-2xl">
            <span className="text-[#A6B5BD]">curl</span> https://api.pseudonymize.io/v1/text \<br/>
            &nbsp;&nbsp;-H <span className="text-[#78AFFF]">"Authorization: Bearer $PZ_API_KEY"</span> \<br/>
            &nbsp;&nbsp;-H <span className="text-[#78AFFF]">"Content-Type: application/json"</span> \<br/>
            &nbsp;&nbsp;-d '&#123;<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#78AFFF]">"text"</span>: <span className="text-[#48D6B0]">"Alice lives in Munich"</span>,<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#78AFFF]">"policy"</span>: <span className="text-[#48D6B0]">"default"</span><br/>
            &nbsp;&nbsp;&#125;'<br/>
            <br/>
            &#123;<br/>
            &nbsp;&nbsp;<span className="text-[#78AFFF]">"text"</span>: <span className="text-[#48D6B0]">"PERSON_7F2A lives in CITY_03E4"</span>,<br/>
            &nbsp;&nbsp;<span className="text-[#78AFFF]">"entities"</span>: 2<br/>
            &#125;
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-24 border-t border-[var(--pz-border)]">
        <div className="pz-container px-4 sm:px-6">
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-10">
            <div>
              <div className="text-[var(--pz-cipher)] font-mono text-xs font-semibold mb-4">01</div>
              <h3 className="text-lg font-semibold text-[var(--pz-text)] mb-2">{t('authHeading')}</h3>
              <p className="text-sm text-[var(--pz-text-secondary)]">{t('authDesc')}</p>
            </div>
            <div>
              <div className="text-[var(--pz-cipher)] font-mono text-xs font-semibold mb-4">02</div>
              <h3 className="text-lg font-semibold text-[var(--pz-text)] mb-2">{t('inputsHeading')}</h3>
              <p className="text-sm text-[var(--pz-text-secondary)]">{t('inputsDesc')}</p>
            </div>
            <div>
              <div className="text-[var(--pz-cipher)] font-mono text-xs font-semibold mb-4">03</div>
              <h3 className="text-lg font-semibold text-[var(--pz-text)] mb-2">{t('errorsHeading')}</h3>
              <p className="text-sm text-[var(--pz-text-secondary)]">{t('errorsDesc')}</p>
            </div>
            <div>
              <div className="text-[var(--pz-cipher)] font-mono text-xs font-semibold mb-4">04</div>
              <h3 className="text-lg font-semibold text-[var(--pz-text)] mb-2">{t('sdksHeading')}</h3>
              <p className="text-sm text-[var(--pz-text-secondary)]">{t('sdksDesc')}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}