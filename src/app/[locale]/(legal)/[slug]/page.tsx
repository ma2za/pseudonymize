import { getTranslations, setRequestLocale } from 'next-intl/server';
import { getLegalDoc } from '@/lib/legal';
import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import { routing } from '@/i18n/routing';
import { Link } from '@/i18n/routing';

type Props = {
  params: Promise<{ locale: string; slug: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, slug } = await params;
  const doc = await getLegalDoc(slug, locale);

  if (!doc) {
    return { title: 'Not Found' };
  }

  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';
  
  const alternates: Record<string, string> = {
    'x-default': `${baseUrl}/${slug}`,
  };
  routing.locales.forEach((l) => {
      alternates[l] = `${baseUrl}/${l}/${slug}`;
  });

  return {
    title: doc.title,
    alternates: {
      canonical: `${baseUrl}/${locale}/${slug}`,
      languages: alternates,
    },
  };
}

export function generateStaticParams() {
  return [
    { slug: 'privacy' },
    { slug: 'terms' }
  ];
}

export default async function LegalPage({ params }: Props) {
  const { locale, slug } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Global');

  const doc = await getLegalDoc(slug, locale);

  if (!doc) {
    notFound();
  }

  return (
    <div className="bg-[var(--pz-surface)] min-h-[100dvh] py-16 sm:py-24 border-t border-[var(--pz-border)]">
      <main className="mx-auto max-w-3xl px-6 lg:px-8">
        <Link href="/" className="text-sm font-semibold leading-6 text-[var(--pz-cipher-strong)] hover:text-[var(--pz-cipher)] transition-colors mb-8 inline-block">
          {t('backToHome') || '← Back to Home'}
        </Link>
        <article>
          <header className="mb-10 border-b border-[var(--pz-border)] pb-6">
            <h1 className="text-3xl font-bold tracking-tight text-[var(--pz-text)] sm:text-4xl">{doc.title}</h1>
            <div className="mt-2 text-sm text-[var(--pz-text-secondary)]">
              Last Updated: <time dateTime={doc.lastUpdated}>{new Date(doc.lastUpdated).toLocaleDateString()}</time>
            </div>
          </header>
          
          <div 
            className="prose prose-lg dark:prose-invert max-w-none text-[var(--pz-text)] prose-headings:text-[var(--pz-text)] prose-a:text-[var(--pz-cipher)] hover:prose-a:text-[var(--pz-cipher-hover)] prose-strong:text-[var(--pz-text)] prose-ul:text-[var(--pz-text)] prose-li:text-[var(--pz-text)]"
            dangerouslySetInnerHTML={{ __html: doc.content }} 
          />
        </article>
      </main>
    </div>
  );
}