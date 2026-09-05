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
    <div className="bg-white min-h-[100dvh] py-16 sm:py-24">
      <main className="mx-auto max-w-3xl px-6 lg:px-8">
        <Link href="/" className="text-sm font-semibold leading-6 text-blue-600 hover:text-blue-500 mb-8 inline-block">
          {t('backToHome') || '← Back to Home'}
        </Link>
        <article>
          <header className="mb-10 border-b border-gray-200 pb-6">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">{doc.title}</h1>
            <div className="mt-2 text-sm text-gray-500">
              Last Updated: <time dateTime={doc.lastUpdated}>{new Date(doc.lastUpdated).toLocaleDateString()}</time>
            </div>
          </header>
          
          <div 
            className="prose prose-lg prose-blue max-w-none text-gray-700"
            dangerouslySetInnerHTML={{ __html: doc.content }} 
          />
        </article>
      </main>
    </div>
  );
}