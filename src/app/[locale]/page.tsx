/* eslint-disable react/no-unescaped-entities */
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
          <div className="text-xs uppercase tracking-widest text-[var(--pz-text-secondary)] mb-4">{t('yourApplication')}</div>
          <p className="pz-sample-line">{t('sampleEmailText1')}<EntityHighlight>{t('sampleName')}</EntityHighlight>{t('sampleEmailText2')}</p>
          <p className="pz-sample-line mb-6"><EntityHighlight>{t('sampleEmailAddress')}</EntityHighlight>{t('sampleEmailText3')}</p>

          <div className="flex flex-col gap-2 my-6 py-6 border-y border-[var(--pz-border)] relative">
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-[var(--pz-border-strong)] text-xs uppercase tracking-widest bg-[var(--pz-canvas)] px-2">{t('pseudonymization')}</div>
            <TransformationRow label={t('sampleNameLabel')} raw={t('sampleName')} pseudonym="PERSON_01" />
            <TransformationRow label={t('sampleEmailLabel')} raw={t('sampleEmailAddress')} pseudonym="EMAIL_01" />
          </div>

          <p className="pz-sample-line">{t('sampleEmailText1')}<PseudonymToken>PERSON_01</PseudonymToken>{t('sampleEmailText2')}</p>
          <p className="pz-sample-line mb-6"><PseudonymToken>EMAIL_01</PseudonymToken>{t('sampleEmailText3')}</p>
          <div className="text-xs uppercase tracking-widest text-[var(--pz-cipher-strong)] mt-4">{t('externalApi')}</div>
        </ProcessorFrame>
      </section>

      {/* 1.5. Boundary Section */}
      <section className="py-24 border-t border-[var(--pz-border)] bg-[var(--pz-surface)] text-center">
        <div className="pz-container px-4 sm:px-6">
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

      {/* 2. Predictable Transformations Section */}
      <section className="py-24 border-t border-[var(--pz-border)]">
        <div className="pz-container px-4 sm:px-6">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl font-bold mb-4">{t('predictableTitle')}</h2>
            <p className="text-lg text-[var(--pz-text-secondary)]">{t('predictableSubtitle')}</p>
          </div>
          <div className="grid md:grid-cols-2 gap-12 lg:gap-16">
            
            <div>
              <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-[var(--pz-cipher)]"></span>
                {t('featIdentityTitle')}
              </h3>
              <p className="text-[var(--pz-text-secondary)] mb-6">{t('featIdentityDesc')}</p>
              <div className="bg-[var(--pz-surface-inset)] border border-[var(--pz-border-strong)] rounded-lg p-5 font-mono text-sm text-[var(--pz-text)] shadow-sm">
                Alice opened ticket #182<br/>
                Alice requested a refund<br/>
                <div className="my-3 text-[var(--pz-cipher)] font-bold">&darr;</div>
                <span className="text-[var(--pz-cipher-strong)]">PERSON_01</span> opened ticket #182<br/>
                <span className="text-[var(--pz-cipher-strong)]">PERSON_01</span> requested a refund
              </div>
            </div>

            <div>
              <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-[var(--pz-cipher)]"></span>
                {t('featStructureTitle')}
              </h3>
              <p className="text-[var(--pz-text-secondary)] mb-6">{t('featStructureDesc')}</p>
              <div className="bg-[var(--pz-surface-inset)] border border-[var(--pz-border-strong)] rounded-lg p-5 font-mono text-sm text-[var(--pz-text)] shadow-sm overflow-x-auto">
                <span className="text-[var(--pz-text-muted)]">&#123;</span><br/>
                &nbsp;&nbsp;<span className="text-[#78AFFF]">"user"</span>: <span className="text-[var(--pz-text-muted)]">&#123;</span><br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#78AFFF]">"name"</span>: <span className="text-[var(--pz-cipher-strong)]">"PERSON_01"</span>,<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#78AFFF]">"email"</span>: <span className="text-[var(--pz-cipher-strong)]">"EMAIL_01"</span><br/>
                &nbsp;&nbsp;<span className="text-[var(--pz-text-muted)]">&#125;</span>,<br/>
                &nbsp;&nbsp;<span className="text-[#78AFFF]">"ticket_id"</span>: <span className="text-[#48D6B0]">"TK-4821"</span><br/>
                <span className="text-[var(--pz-text-muted)]">&#125;</span>
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-[var(--pz-cipher)]"></span>
                {t('featPolicyTitle')}
              </h3>
              <p className="text-[var(--pz-text-secondary)] mb-6">{t('featPolicyDesc')}</p>
              <div className="bg-[var(--pz-surface-inset)] border border-[var(--pz-border-strong)] rounded-lg p-5 font-mono text-sm text-[var(--pz-text)] shadow-sm">
                <span className="text-[var(--pz-text-muted)]">&#123;</span><br/>
                &nbsp;&nbsp;<span className="text-[#78AFFF]">"entities"</span>: [<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#48D6B0]">"person"</span>,<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#48D6B0]">"email"</span>,<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#48D6B0]">"phone"</span>,<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#48D6B0]">"iban"</span><br/>
                &nbsp;&nbsp;]<br/>
                <span className="text-[var(--pz-text-muted)]">&#125;</span>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-[var(--pz-cipher)]"></span>
                {t('featDeployTitle')}
              </h3>
              <p className="text-[var(--pz-text-secondary)] mb-6">{t('featDeployDesc')}</p>
              <div className="flex gap-4">
                 <Link href="/docs" className="text-sm font-semibold leading-6 text-[var(--pz-cipher-strong)] hover:text-[var(--pz-cipher)] transition-colors">
                    {t('exploreApiDocs')} <span aria-hidden="true">→</span>
                 </Link>
                 <a href="https://github.com/ma2za/pseudonymize" className="text-sm font-semibold leading-6 text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
                    {t('viewGithub')} <span aria-hidden="true">→</span>
                 </a>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* 3. Redaction vs Pseudonymization Section */}
      <section className="py-24 bg-[var(--pz-surface)] border-t border-[var(--pz-border)]">
        <div className="pz-container px-4 sm:px-6 text-center max-w-4xl">
          <h2 className="text-3xl font-bold mb-16 leading-tight">{t('redactionTitle')}</h2>
          <div className="grid md:grid-cols-3 gap-px bg-[var(--pz-border)] border border-[var(--pz-border)] rounded-xl overflow-hidden shadow-sm">
            <div className="bg-[var(--pz-canvas)] p-8 text-left">
              <h3 className="text-sm uppercase tracking-widest font-semibold mb-6 text-[var(--pz-text-muted)]">{t('original')}</h3>
              <div className="font-mono text-sm leading-loose text-[var(--pz-text)]">
                {t('redactionOriginal')}
              </div>
            </div>
            <div className="bg-[var(--pz-canvas)] p-8 text-left">
              <h3 className="text-sm uppercase tracking-widest font-semibold mb-6 text-[var(--pz-danger)]">{t('redaction')}</h3>
              <div className="font-mono text-sm leading-loose text-[var(--pz-text-secondary)] line-through decoration-[var(--pz-danger)] opacity-80">
                {t('redactionMasked')}
              </div>
            </div>
            <div className="bg-[var(--pz-canvas)] p-8 text-left">
              <h3 className="text-sm uppercase tracking-widest font-semibold mb-6 text-[var(--pz-cipher-strong)]">{t('pseudonymization')}</h3>
              <div className="font-mono text-sm leading-loose text-[var(--pz-text)] font-semibold text-[var(--pz-cipher-strong)]">
                {t('redactionPseudonymized')}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Developers Section */}
      <section className="py-24 bg-[var(--pz-ink)] text-white border-t border-[var(--pz-border)]">
        <div className="pz-container px-4 sm:px-6 grid md:grid-cols-2 gap-12 align-middle items-center">
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

      {/* 5. Trust Section (Operational Characteristics) */}
      <section className="py-24 border-t border-[var(--pz-border)]">
        <div className="pz-container px-4 sm:px-6 text-center">
          <h2 className="text-3xl font-bold mb-12">{t('trustTitle')}</h2>
          <TrustFacts facts={[
            { label: t('trust1Label'), value: t('trust1') },
            { label: t('trust2Label'), value: t('trust2') },
            { label: t('trust3Label'), value: t('trust3') }
          ]} />
        </div>
      </section>

      {/* 6. Final CTA */}
      <section className="py-32 bg-[var(--pz-surface)] border-t border-[var(--pz-border)] text-center">
        <div className="pz-container px-4 sm:px-6">
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