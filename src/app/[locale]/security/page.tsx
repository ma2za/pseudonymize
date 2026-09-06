import { getTranslations, setRequestLocale } from 'next-intl/server';
import type { Metadata } from 'next';
import { routing } from '@/i18n/routing';
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { remark } from 'remark';
import html from 'remark-html';
import { notFound } from 'next/navigation';

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({locale, namespace: 'Security'});
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';

  const alternates: Record<string, string> = {
    'x-default': `${baseUrl}/security`,
  };
  routing.locales.forEach((l) => {
      alternates[l] = `${baseUrl}/${l}/security`;
  });

  const title = `${t('title')} | pseudonymize.io`;
  const description = t('description');

  return {
    title,
    description,
    alternates: {
      canonical: `${baseUrl}/${locale}/security`,
      languages: alternates,
    },
    openGraph: {
      title,
      description,
      url: `${baseUrl}/${locale}/security`,
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

async function getSecurityContent(locale: string) {
  const secDirectory = path.join(process.cwd(), 'content', 'security');
  const localeDir = path.join(secDirectory, locale);
  let targetDir = localeDir;
  let fullPath = path.join(targetDir, 'index.md');

  if (!fs.existsSync(fullPath)) {
    targetDir = path.join(secDirectory, 'en');
    fullPath = path.join(targetDir, 'index.md');
  }

  if (!fs.existsSync(fullPath)) {
    return null;
  }

  const fileContents = fs.readFileSync(fullPath, 'utf8');
  const matterResult = matter(fileContents);

  const processedContent = await remark()
    .use(html)
    .process(matterResult.content);
    
  return processedContent.toString();
}

export default async function SecurityPage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);

  const contentHtml = await getSecurityContent(locale);
  if (!contentHtml) {
    notFound();
  }

  return (
    <div className="bg-[var(--pz-surface)] min-h-[100dvh] py-16 sm:py-24 border-t border-[var(--pz-border)]">
      <main className="mx-auto max-w-4xl px-6 lg:px-8">
        <article className="prose prose-lg dark:prose-invert max-w-none text-[var(--pz-text)] prose-headings:text-[var(--pz-text)] prose-a:text-[var(--pz-cipher)] hover:prose-a:text-[var(--pz-cipher-hover)] prose-code:text-[var(--pz-cipher-strong)] prose-pre:bg-[var(--pz-canvas)] prose-pre:border prose-pre:border-[var(--pz-border-strong)] prose-hr:border-[var(--pz-border)]">
          <div dangerouslySetInnerHTML={{ __html: contentHtml }} />
        </article>
      </main>
    </div>
  );
}