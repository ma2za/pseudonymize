import { useLocale } from 'next-intl';
import { ChangeEvent, useState } from 'react';
import { Globe, ChevronDown } from 'lucide-react';

const locales = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Español' },
  { code: 'fr', name: 'Français' },
  { code: 'de', name: 'Deutsch' },
  { code: 'it', name: 'Italiano' },
  { code: 'pt', name: 'Português' },
  { code: 'nl', name: 'Nederlands' },
  { code: 'ru', name: 'Русский' },
  { code: 'zh', name: '中文' },
  { code: 'ja', name: '日本語' },
  { code: 'ko', name: '한국語' },
  { code: 'ar', name: 'العربية' },
  { code: 'hi', name: 'हिन्दी' },
  { code: 'tr', name: 'Türkçe' },
  { code: 'pl', name: 'Polski' },
  { code: 'sv', name: 'Svenska' },
  { code: 'no', name: 'Norsk' },
  { code: 'da', name: 'Dansk' },
  { code: 'fi', name: 'Suomi' },
  { code: 'el', name: 'Ελληνικά' },
];

export default function LanguageSwitcher() {
  const currentLocale = useLocale();
  const [isPending, setIsPending] = useState(false);

  const onSelectChange = (e: ChangeEvent<HTMLSelectElement>) => {
    setIsPending(true);
    const nextLocale = e.target.value;
    
    // Bulletproof language switching via hard navigation
    // This avoids any SPA router caching bugs or missing params on dynamic routes
    const currentPath = window.location.pathname;
    
    // Check if the path starts with the current locale
    const regex = new RegExp(`^/${currentLocale}(/|$)`);
    let newPath = currentPath;
    
    if (regex.test(currentPath)) {
      newPath = currentPath.replace(`/${currentLocale}`, `/${nextLocale}`);
    } else {
      // Fallback if somehow there's no locale in the URL
      newPath = `/${nextLocale}${currentPath}`;
    }
    
    // Preserve search params (e.g. ?success=true)
    window.location.href = newPath + window.location.search;
  };

  return (
    <div className="relative inline-flex items-center text-[var(--pz-text-secondary)] hover:text-[var(--pz-text)] transition-colors">
      <Globe className="w-4 h-4 absolute left-2 pointer-events-none" />
      <select
        className="appearance-none bg-transparent py-2 pl-8 pr-8 text-sm font-medium cursor-pointer outline-none focus:ring-2 focus:ring-[var(--pz-cipher)] rounded-md disabled:opacity-50 max-w-[100px] sm:max-w-none truncate"
        value={currentLocale}
        disabled={isPending}
        onChange={onSelectChange}
        aria-label="Select language"
      >
        {locales.map((locale) => (
          <option key={locale.code} value={locale.code} className="text-[var(--pz-ink)] bg-[var(--pz-canvas)]">
            {locale.name}
          </option>
        ))}
      </select>
      <ChevronDown className="w-4 h-4 absolute right-2 pointer-events-none opacity-60" />
    </div>
  );
}