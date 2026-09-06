import { getTranslations, setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { Link } from '@/i18n/routing';
import type { Metadata } from 'next';
import { routing } from '@/i18n/routing';
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { remark } from 'remark';
import html from 'remark-html';

type Props = {
  params: Promise<{ locale: string; slug: string[] }>;
};

async function getDocPage(slug: string[], locale: string) {
  const docsDirectory = path.join(process.cwd(), 'content', 'docs');
  const slugPath = slug.join('/');
  
  let fullPath = path.join(docsDirectory, locale, `${slugPath}.md`);

  if (!fs.existsSync(fullPath)) {
    fullPath = path.join(docsDirectory, 'en', `${slugPath}.md`);
  }

  if (!fs.existsSync(fullPath)) {
    return null;
  }

  const fileContents = fs.readFileSync(fullPath, 'utf8');
  const matterResult = matter(fileContents);

  const processedContent = await remark()
    .use(html)
    .process(matterResult.content);

  return {
    title: matterResult.data.title || slug[slug.length - 1],
    content: processedContent.toString(),
  };
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, slug } = await params;
  const doc = await getDocPage(slug, locale);

  if (!doc) {
    return { title: 'Not Found' };
  }

  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';
  const slugPath = slug.join('/');
  
  const alternates: Record<string, string> = {
    'x-default': `${baseUrl}/docs/${slugPath}`,
  };
  routing.locales.forEach((l) => {
      alternates[l] = `${baseUrl}/${l}/docs/${slugPath}`;
  });

  const description = `Read about ${doc.title} in the pseudonymize.io developer documentation.`;
  return {
    title: doc.title,
    description,
    alternates: {
      canonical: `${baseUrl}/${locale}/docs/${slugPath}`,
      languages: alternates,
    },
    openGraph: {
      title: doc.title,
      description,
      url: `${baseUrl}/${locale}/docs/${slugPath}`,
      type: 'article',
      siteName: 'pseudonymize.io',
    },
    twitter: {
      card: 'summary_large_image',
      title: doc.title,
      description,
    }
  };
}

export default async function DocPage({ params }: Props) {
  const { locale, slug } = await params;
  setRequestLocale(locale);

  const doc = await getDocPage(slug, locale);

  if (!doc) {
    notFound();
  }

  return (
    <div className="bg-[var(--pz-surface)] min-h-[100dvh] py-16 sm:py-24 border-t border-[var(--pz-border)]">
      <main className="mx-auto max-w-4xl px-6 lg:px-8">
        <Link href="/docs" className="text-sm font-semibold leading-6 text-[var(--pz-cipher-strong)] hover:text-[var(--pz-cipher)] transition-colors mb-8 inline-block">
          ← Back to Docs
        </Link>
        <article>
          <div 
            className="prose prose-lg dark:prose-invert max-w-none text-[var(--pz-text)] prose-headings:text-[var(--pz-text)] prose-a:text-[var(--pz-cipher)] hover:prose-a:text-[var(--pz-cipher-hover)] prose-strong:text-[var(--pz-text)] prose-ul:text-[var(--pz-text)] prose-li:text-[var(--pz-text)] prose-code:text-[var(--pz-cipher-strong)] prose-pre:bg-[var(--pz-canvas)] prose-pre:border prose-pre:border-[var(--pz-border-strong)]"
            dangerouslySetInnerHTML={{ __html: doc.content }} 
          />
        </article>
      </main>
    </div>
  );
}