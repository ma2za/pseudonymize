import { BrandButton, EntityHighlight, ProcessorFrame, PseudonymToken, TransformationRow } from '../components'
import { brandCopy } from '../copy'

export function HomeHero() {
  return (
    <section className="pz-home-hero">
      <div className="pz-home-hero__copy">
        <p className="pz-eyebrow">{brandCopy.homepage.eyebrow}</p>
        <h1>{brandCopy.homepage.h1}</h1>
        <p className="pz-lead">{brandCopy.homepage.lead}</p>
        <div className="pz-actions"><BrandButton>{brandCopy.homepage.primaryCta}</BrandButton><BrandButton variant="secondary">{brandCopy.homepage.secondaryCta}</BrandButton></div>
      </div>
      <ProcessorFrame>
        <p className="pz-sample-line">Email <EntityHighlight>alice@example.com</EntityHighlight> about invoice INV-204.</p>
        <TransformationRow label="Email" raw="alice@example.com" pseudonym="EMAIL_01" />
        <p className="pz-sample-line">Email <PseudonymToken>EMAIL_01</PseudonymToken> about invoice INV-204.</p>
      </ProcessorFrame>
    </section>
  )
}
