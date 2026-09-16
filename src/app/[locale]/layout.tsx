import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import {NextIntlClientProvider} from 'next-intl';
import {getMessages, setRequestLocale, getTranslations} from 'next-intl/server';
import {routing} from '@/i18n/routing';
import { notFound } from "next/navigation";
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { ThemeProvider } from "@/components/ThemeProvider";
import { PostHogProvider } from '@/components/PostHogProvider';

import { auth } from '@/lib/auth';
import { headers } from 'next/headers';

const inter = Inter({ subsets: ["latin"] });

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({locale, namespace: 'Home'});
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';

  const alternates: Record<string, string> = {
    'x-default': baseUrl,
  };
  routing.locales.forEach((l) => {
      alternates[l] = `${baseUrl}/${l}`;
  });

  return {
    title: {
      template: '%s | pseudonymize.io',
      default: t('title') || 'pseudonymize.io',
    },
    description: t('description'),
    metadataBase: new URL(baseUrl),
    alternates: {
      canonical: `${baseUrl}/${locale}`,
      languages: alternates,
    },
    openGraph: {
      title: t('title'),
      description: t('description'),
      url: `${baseUrl}/${locale}`,
      siteName: 'pseudonymize.io',
      locale: locale,
      type: 'website',
    },
    twitter: {
      card: 'summary_large_image',
      title: t('title'),
      description: t('description'),
    },
    robots: {
      index: true,
      follow: true,
      googleBot: {
        index: true,
        follow: true,
        'max-video-preview': -1,
        'max-image-preview': 'large',
        'max-snippet': -1,
      },
    },
    icons: {
      icon: '/brand/favicon.svg',
    },
  };
}

export function generateStaticParams() {
  return routing.locales.map((locale) => ({locale}));
}

export default async function RootLayout({
  children,
  params
}: Readonly<{
  children: React.ReactNode;
  params: Promise<{locale: string}>;
}>) {
  const { locale } = await params;
  if (!(routing.locales as readonly string[]).includes(locale)) {
    notFound();
  }

  setRequestLocale(locale);
  const messages = await getMessages();

  const session = await auth.api.getSession({
    headers: await headers()
  });

  // Suppress hydration warning on HTML tag because next-themes manipulates it
  return (
    <html lang={locale} suppressHydrationWarning>
      <body className={`${inter.className} bg-[var(--pz-canvas)] text-[var(--pz-text)] antialiased flex flex-col min-h-screen`}>
        <PostHogProvider>
          <ThemeProvider attribute="data-theme" defaultTheme="system" enableSystem disableTransitionOnChange>   
            <NextIntlClientProvider messages={messages}>
              <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-[var(--pz-cipher)] focus:text-[var(--pz-ink)] focus:rounded-md focus:font-semibold">
                Skip to content
              </a>
              <Header session={session} />
              <main id="main-content" tabIndex={-1} className="flex-1 focus:outline-none">
                {children}
              </main>
              <Footer />
            </NextIntlClientProvider>
          </ThemeProvider>
        </PostHogProvider>
      </body>
    </html>
  );
}