import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Link } from '@/i18n/routing';
import { BrandButton, EntityHighlight, ProcessorFrame, PseudonymToken, TransformationRow, TrustFacts } from '@/brand/components';

export default async function HomePage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Home');

  return (
    <div className="pz-appbody">
      {/* 1. Hero Section */}
      <section className="pz-home-hero">
        <div className="pz-home-hero__copy">
          <p className="pz-eyebrow">{t('eyebrow')}</p>
          <h1>{t('title')}</h1>
          <p className="pz-lead">{t('description')}</p>
          <div className="pz-actions">
            <Link href="/signup" style={{ textDecoration: 'none' }}>
              <BrandButton>{t('getStarted')}</BrandButton>
            </Link>
            <Link href="/docs" style={{ textDecoration: 'none' }}>
              <BrandButton variant="secondary">{t('viewOpenSource')}</BrandButton>
            </Link>
          </div>
        </div>
        <ProcessorFrame>
          <div className="text-xs uppercase tracking-widest text-[var(--pz-text-secondary)] mb-4">Your application</div>
          <p className="pz-sample-line">{t('sampleEmailText1')}<EntityHighlight>{t('sampleName')}</EntityHighlight>{t('sampleEmailText2')}</p>
          <p className="pz-sample-line mb-6"><EntityHighlight>{t('sampleEmailAddress')}</EntityHighlight>{t('sampleEmailText3')}</p>

          <div className="flex flex-col gap-2 my-6 py-6 border-y border-[var(--pz-border)] relative">
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-[var(--pz-border-strong)] text-xs uppercase tracking-widest bg-[var(--pz-canvas)] px-2">Pseudonymize</div>
            <TransformationRow label={t('sampleNameLabel')} raw={t('sampleName')} pseudonym="PERSON_01" />
            <TransformationRow label={t('sampleEmailLabel')} raw={t('sampleEmailAddress')} pseudonym="EMAIL_01" />
          </div>

          <p className="pz-sample-line">{t('sampleEmailText1')}<PseudonymToken>PERSON_01</PseudonymToken>{t('sampleEmailText2')}</p>
          <p className="pz-sample-line mb-6"><PseudonymToken>EMAIL_01</PseudonymToken>{t('sampleEmailText3')}</p>
          <div className="text-xs uppercase tracking-widest text-[var(--pz-cipher-strong)] mt-4">OpenAI / Anthropic / Gemini / external API</div>
        </ProcessorFrame>
      </section>

      {/* 1.5. Boundary Section */}
      <section className="py-24 border-t border-[var(--pz-border)] bg-[var(--pz-surface)] text-center">
        <div className="pz-container">
          <h2 className="text-3xl font-bold mb-12">{t('workflowBoundaryTitle')}</h2>
          <div className="grid md:grid-cols-3 gap-8 text-[var(--pz-text-secondary)] font-mono text-sm">
            <div className="px-6 py-6 border border-[var(--pz-border-strong)] rounded-lg bg-[var(--pz-canvas)]">
              <div className="text-[var(--pz-text-primary)] font-bold mb-4 font-sans tracking-wide">AI</div>
              {t('workflowBoundaryAI')}
            </div>
            <div className="px-6 py-6 border border-[var(--pz-border-strong)] rounded-lg bg-[var(--pz-canvas)]">
              <div className="text-[var(--pz-text-primary)] font-bold mb-4 font-sans tracking-wide">Analytics</div>
              {t('workflowBoundaryAnalytics')}
            </div>
            <div className="px-6 py-6 border border-[var(--pz-border-strong)] rounded-lg bg-[var(--pz-canvas)]">
              <div className="text-[var(--pz-text-primary)] font-bold mb-4 font-sans tracking-wide">Support</div>
              {t('workflowBoundarySupport')}
            </div>
          </div>
        </div>
      </section>

      {/* 2. Inputs Section */}
      <section className="py-24 border-t border-[var(--pz-border)] text-center">
        <div className="pz-container">
          <h2 className="text-3xl font-bold mb-12">{t('inputsTitle')}</h2>
          <div className="flex flex-col sm:flex-row justify-center gap-8 text-[var(--pz-text-secondary)] font-mono text-sm">
            <div className="px-6 py-4 border border-[var(--pz-border-strong)] rounded-lg bg-[var(--pz-surface-inset)]">
              [ {t('inputsText')} ]
            </div>
            <div className="px-6 py-4 border border-[var(--pz-border-strong)] rounded-lg bg-[var(--pz-surface-inset)]">
              [ {t('inputsStructured')} ]
            </div>
            <div className="px-6 py-4 border border-[var(--pz-border-strong)] rounded-lg bg-[var(--pz-surface-inset)]">
              [ {t('inputsFiles')} ]
            </div>
          </div>
        </div>
      </section>

      {/* 3. Proof Section */}
      <section className="py-24 bg-[var(--pz-surface)] border-t border-[var(--pz-border)]">
        <div className="pz-container">
          <h2 className="text-3xl font-bold mb-16 text-center">{t('proofTitle')}</h2>
          <div className="grid sm:grid-cols-2 gap-px bg-[var(--pz-border)] border border-[var(--pz-border)] rounded-xl overflow-hidden">
            <div className="bg-[var(--pz-canvas)] p-8">
              <h3 className="text-lg font-semibold mb-6">{t('proofOriginal')}</h3>
              <div className="font-mono text-sm leading-loose text-[var(--pz-text-secondary)]">
                User <EntityHighlight>Alice</EntityHighlight> logged in from <EntityHighlight>Munich</EntityHighlight>.<br/>
                Contact: <EntityHighlight>alice@example.com</EntityHighlight>
              </div>
            </div>
            <div className="bg-[var(--pz-canvas)] p-8">
              <h3 className="text-lg font-semibold mb-6 text-[var(--pz-cipher-strong)]">{t('proofPseudonymized')}</h3>
              <div className="font-mono text-sm leading-loose text-[var(--pz-text-secondary)]">
                User <PseudonymToken>PERSON_01</PseudonymToken> logged in from <PseudonymToken>CITY_01</PseudonymToken>.<br/>
                Contact: <PseudonymToken>EMAIL_01</PseudonymToken>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Workflow Section */}
      <section className="py-24 border-t border-[var(--pz-border)] text-center">
        <div className="pz-container">
          <h2 className="text-3xl font-bold mb-12">{t('workflowTitle')}</h2>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 text-sm font-mono text-[var(--pz-text-secondary)]">
            <div className="px-6 py-3 bg-[var(--pz-surface)] border border-[var(--pz-border)] rounded-full">1. {t('workflowStep1')}</div>
            <span className="text-[var(--pz-border-strong)]">&rarr;</span>
            <div className="px-6 py-3 bg-[var(--pz-surface)] border border-[var(--pz-border)] rounded-full text-[var(--pz-cipher-strong)]">2. {t('workflowStep2')}</div>
            <span className="text-[var(--pz-border-strong)]">&rarr;</span>
            <div className="px-6 py-3 bg-[var(--pz-surface)] border border-[var(--pz-border)] rounded-full">3. {t('workflowStep3')}</div>
          </div>
        </div>
      </section>

      {/* 5. Developers Section */}
      <section className="py-24 bg-[var(--pz-ink)] text-white border-t border-[var(--pz-border)]">
        <div className="pz-container grid md:grid-cols-2 gap-12 align-middle items-center">
          <div>
            <h2 className="text-3xl font-bold mb-6 text-[var(--pz-canvas)]">{t('developersTitle')}</h2>
            <Link href="/docs" style={{ textDecoration: 'none' }}>
              <BrandButton>{t('developersCta')}</BrandButton>
            </Link>
          </div>
          <div className="bg-[#050A0F] border border-[#172630] rounded-xl p-6 font-mono text-xs text-[#758690] overflow-x-auto shadow-2xl">
            <span className="text-[#A6B5BD]">curl</span> https://api.pseudonymize.io/v1/text \<br/>
            &nbsp;&nbsp;-H <span className="text-[#78AFFF]">"Authorization: Bearer $PZ_API_KEY"</span> \<br/>
            &nbsp;&nbsp;-H <span className="text-[#78AFFF]">"Content-Type: application/json"</span> \<br/>
            &nbsp;&nbsp;-d '&#123;<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#78AFFF]">"text"</span>: <span className="text-[#48D6B0]">"Alice lives in Munich"</span>,<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#78AFFF]">"policy"</span>: <span className="text-[#48D6B0]">"default"</span><br/>
            &nbsp;&nbsp;&#125;'
          </div>
        </div>
      </section>

      {/* 6. Trust Section */}
      <section className="py-24 border-t border-[var(--pz-border)]">
        <div className="pz-container text-center">
          <h2 className="text-3xl font-bold mb-12">{t('trustTitle')}</h2>
          <TrustFacts facts={[
            { label: 'Data Retention', value: t('trust1') },
            { label: 'Data Processing', value: t('trust2') }
          ]} />
        </div>
      </section>

      {/* 7. Final CTA */}
      <section className="py-32 bg-[var(--pz-surface)] border-t border-[var(--pz-border)] text-center">
        <div className="pz-container">
          <h2 className="text-4xl sm:text-5xl font-bold mb-10 max-w-2xl mx-auto leading-tight">{t('finalTitle')}</h2>
          <div className="pz-actions justify-center">
            <Link href="/signup" style={{ textDecoration: 'none' }}>
              <BrandButton>{t('finalPrimary')}</BrandButton>
            </Link>
            <Link href="/docs" style={{ textDecoration: 'none' }}>
              <BrandButton variant="secondary">{t('finalSecondary')}</BrandButton>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}