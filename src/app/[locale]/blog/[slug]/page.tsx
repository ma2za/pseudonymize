import { getTranslations, setRequestLocale } from 'next-intl/server';
import { getBlogPost, getBlogPosts } from '@/lib/cms';
import { notFound } from 'next/navigation';
import { Link } from '@/i18n/routing';
import type { Metadata } from 'next';
import { routing } from '@/i18n/routing';

type Props = {
  params: Promise<{ locale: string; slug: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, slug } = await params;
  const post = await getBlogPost(slug, locale);

  if (!post) {
    return { title: 'Not Found' };
  }

  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';
  
  const alternates: Record<string, string> = {
    'x-default': `${baseUrl}/blog/${slug}`,
  };
  routing.locales.forEach((l) => {
      alternates[l] = `${baseUrl}/${l}/blog/${slug}`;
  });

  return {
    title: post.title,
    description: post.excerpt,
    alternates: {
      canonical: `${baseUrl}/${locale}/blog/${slug}`,
      languages: alternates,
    },
    openGraph: {
      title: post.title,
      description: post.excerpt,
      url: `${baseUrl}/${locale}/blog/${slug}`,
      type: 'article',
      publishedTime: post.date,
    }
  };
}

export async function generateStaticParams({ params }: { params: { locale: string } }) {
  // In Next.js 15 app router typings, `generateStaticParams` receives the unwrapped params from the parent segments.
  const locale = params.locale;
  const posts = getBlogPosts(locale);

  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export default async function BlogPostPage({ params }: Props) {
  const { locale, slug } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Blog');

  const post = await getBlogPost(slug, locale);

  if (!post) {
    notFound();
  }

  return (
    <div className="bg-white min-h-screen py-16 sm:py-24">
      <main className="mx-auto max-w-3xl px-6 lg:px-8">
        <Link href="/blog" className="text-sm font-semibold leading-6 text-blue-600 hover:text-blue-500 mb-8 inline-block">
          {t('backToBlog')}
        </Link>
        <article>
          <header className="mb-10">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">{post.title}</h1>
            <div className="mt-4 flex items-center gap-x-4 text-sm text-gray-500">
              <time dateTime={post.date}>{new Date(post.date).toLocaleDateString()}</time>
            </div>
          </header>
          
          <div 
            className="prose prose-lg prose-blue max-w-none text-gray-700"
            dangerouslySetInnerHTML={{ __html: post.content }} 
          />
        </article>
      </main>
    </div>
  );
}