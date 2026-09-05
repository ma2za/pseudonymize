'use client';

import { useLocale } from 'next-intl';
import { useRouter, usePathname } from '@/i18n/routing';
import { ChangeEvent, useTransition } from 'react';
import { Globe } from 'lucide-react';

const locales = [
  { code: 'en', name: 'EN' },
  { code: 'es', name: 'ES' },
  { code: 'fr', name: 'FR' },
  { code: 'de', name: 'DE' },
  { code: 'it', name: 'IT' },
];

export default function LanguageSwitcher() {
  const [isPending, startTransition] = useTransition();
  const router = useRouter();
  const pathname = usePathname();
  const currentLocale = useLocale();

  const onSelectChange = (e: ChangeEvent<HTMLSelectElement>) => {
    const nextLocale = e.target.value;
    startTransition(() => {
      router.replace(pathname, { locale: nextLocale });
    });
  };

  return (
    <div className="relative inline-flex items-center text-gray-500 hover:text-gray-900">
      <Globe className="w-4 h-4 absolute left-2 pointer-events-none" />
      <select
        className="appearance-none bg-transparent py-1 pl-8 pr-4 text-sm font-semibold cursor-pointer outline-none focus:ring-0"
        defaultValue={currentLocale}
        disabled={isPending}
        onChange={onSelectChange}
        aria-label="Select language"
      >
        {locales.map((locale) => (
          <option key={locale.code} value={locale.code}>
            {locale.name}
          </option>
        ))}
      </select>
    </div>
  );
}