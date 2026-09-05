import { MetadataRoute } from 'next';
import { routing } from '@/i18n/routing';

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';
  
  // Base routes that exist in all languages
  const baseRoutes = [
    '',
    '/login',
  ];

  const sitemapEntries: MetadataRoute.Sitemap = [];

  baseRoutes.forEach((route) => {
    routing.locales.forEach((locale) => {
      const isDefault = locale === routing.defaultLocale;
      const url = `${baseUrl}${isDefault && route === '' ? '' : `/${locale}${route}`}`;

      const alternates: Record<string, string> = {
         'x-default': `${baseUrl}${route}`,
      };

      routing.locales.forEach((altLocale) => {
          alternates[altLocale] = `${baseUrl}/${altLocale}${route}`;
      });

      sitemapEntries.push({
        url,
        lastModified: new Date(),
        changeFrequency: 'weekly',
        priority: route === '' ? 1 : 0.8,
        alternates: {
          languages: alternates,
        },
      });
    });
  });

  return sitemapEntries;
}