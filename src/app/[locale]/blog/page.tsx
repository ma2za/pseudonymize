import { getTranslations, setRequestLocale } from 'next-intl/server';
import { getBlogPosts } from '@/lib/cms';
import { Link } from '@/i18n/routing';
import type { Metadata } from 'next';
import { routing } from '@/i18n/routing';

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({locale, namespace: 'Blog'});
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';

  const alternates: Record<string, string> = {
    'x-default': `${baseUrl}/blog`,
  };
  routing.locales.forEach((l) => {
      alternates[l] = `${baseUrl}/${l}/blog`;
  });

  return {
    title: t('blogTitle'),
    description: t('blogDescription'),
    alternates: {
      canonical: `${baseUrl}/${locale}/blog`,
      languages: alternates,
    },
    openGraph: {
      title: t('blogTitle'),
      description: t('blogDescription'),
      url: `${baseUrl}/${locale}/blog`,
      type: 'website',
    }
  };
}

export default async function BlogIndexPage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Blog');
  
  const posts = getBlogPosts(locale);

  return (
    <div className="bg-gray-50 min-h-screen py-24 sm:py-32">
      <main className="mx-auto max-w-7xl px-6 lg:px-8">
        <header className="mx-auto max-w-2xl lg:mx-0">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">{t('blogTitle')}</h1>
          <p className="mt-2 text-lg leading-8 text-gray-600">
            {t('blogDescription')}
          </p>
        </header>
        <div className="mx-auto mt-10 grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 border-t border-gray-200 pt-10 sm:mt-16 sm:pt-16 lg:mx-0 lg:max-w-none lg:grid-cols-3">
          {posts.map((post) => (
            <article key={post.slug} className="flex max-w-xl flex-col items-start justify-between">
              <div className="flex items-center gap-x-4 text-xs">
                <time dateTime={post.date} className="text-gray-500">
                  {new Date(post.date).toLocaleDateString()}
                </time>
              </div>
              <div className="group relative">
                <h3 className="mt-3 text-lg font-semibold leading-6 text-gray-900 group-hover:text-gray-600">
                  <Link href={`/blog/${post.slug}`}>
                    <span className="absolute inset-0" />
                    {post.title}
                  </Link>
                </h3>
                <p className="mt-5 line-clamp-3 text-sm leading-6 text-gray-600">{post.excerpt}</p>
              </div>
              <div className="mt-4">
                 <Link href={`/blog/${post.slug}`} className="text-sm font-semibold leading-6 text-blue-600 hover:text-blue-500">
                    {t('readMore')} <span aria-hidden="true">→</span>
                 </Link>
              </div>
            </article>
          ))}
        </div>
      </main>
    </div>
  );
}