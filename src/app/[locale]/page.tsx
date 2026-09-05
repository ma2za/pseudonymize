import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Link } from '@/i18n/routing';
import { BrandButton, EntityHighlight, ProcessorFrame, PseudonymToken, TransformationRow } from '@/brand/components';

export default async function HomePage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Home');
  
  return (
    <div className="pz-appbody">
      <section className="pz-home-hero">
        <div className="pz-home-hero__copy">
          <p className="pz-eyebrow">{t('eyebrow')}</p>
          <h1>{t('title')}</h1>
          <p className="pz-lead">{t('description')}</p>
          <div className="pz-actions">
            <Link href="/login" style={{ textDecoration: 'none' }}>
              <BrandButton>{t('getStarted')}</BrandButton>
            </Link>
            <Link href="/blog" style={{ textDecoration: 'none' }}>
              <BrandButton variant="secondary">{t('viewOpenSource')}</BrandButton>
            </Link>
          </div>
        </div>
        <ProcessorFrame>
          <p className="pz-sample-line">{t('sampleEmailText1')}<EntityHighlight>{t('sampleEmailAddress')}</EntityHighlight>{t('sampleEmailText2')}</p>
          <TransformationRow label={t('sampleEmailLabel')} raw={t('sampleEmailAddress')} pseudonym="EMAIL_01" />
          <p className="pz-sample-line">{t('sampleEmailText1')}<PseudonymToken>EMAIL_01</PseudonymToken>{t('sampleEmailText2')}</p>
        </ProcessorFrame>
      </section>
    </div>
  );
}