'use client';
import { useState } from 'react';
import { authClient } from '@/lib/auth-client';
import { Link, usePathname } from '@/i18n/routing';
import { useTranslations, useLocale } from 'next-intl';
import { Eye, EyeOff } from 'lucide-react';
import { BrandButton } from '@/brand/components';

export default function SignupPage() {
  const t = useTranslations('Signup');
  const locale = useLocale();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await authClient.signUp.email({
        name,
        email,
        password,
        fetchOptions: {
          onSuccess: () => {
            // Bulletproof native navigation to avoid React injection bugs (e.g. from Loom/Grammarly extensions)
            window.location.href = `/${locale}/dashboard`;
          },
        },
      });
    } catch (e) {
      setLoading(false);
    }
  };

  const handleGoogleSignup = async () => {
    await authClient.signIn.social({
      provider: "google",
      callbackURL: `/${locale}/dashboard`
    });
  };

  return (
    <div className="flex min-h-[100dvh] flex-col justify-center px-4 py-12 sm:px-6 lg:px-8 bg-[var(--pz-canvas)] overflow-hidden">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-bold leading-9 tracking-tight text-[var(--pz-text)]">
          {t('title')}
        </h2>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        <form className="space-y-6 bg-[var(--pz-surface)] border border-[var(--pz-border)] p-6 sm:p-8 rounded-xl shadow-lg" onSubmit={handleSignup}>
          <div>
            <label htmlFor="name-input" className="block text-sm font-medium leading-6 text-[var(--pz-text-secondary)]">{t('nameLabel')}</label>
            <div className="mt-2">
              <input 
                id="name-input" 
                type="text" 
                required 
                className="block w-full rounded-md border border-[var(--pz-border-strong)] hover:border-[var(--pz-text-muted)] focus:border-[var(--pz-cipher)] py-2.5 text-[var(--pz-text)] bg-[var(--pz-surface-inset)] shadow-sm focus:outline-none focus:ring-2 focus:ring-[var(--pz-cipher)] sm:text-sm sm:leading-6 px-4 transition-all duration-150 cursor-text disabled:opacity-50" 
                value={name} 
                onChange={e => setName(e.target.value)} 
                disabled={loading} 
              />
            </div>
          </div>
          
          <div>
            <label htmlFor="email-input" className="block text-sm font-medium leading-6 text-[var(--pz-text-secondary)]">{t('emailLabel')}</label>
            <div className="mt-2">
              <input 
                id="email-input" 
                type="email" 
                required 
                className="block w-full rounded-md border border-[var(--pz-border-strong)] hover:border-[var(--pz-text-muted)] focus:border-[var(--pz-cipher)] py-2.5 text-[var(--pz-text)] bg-[var(--pz-surface-inset)] shadow-sm focus:outline-none focus:ring-2 focus:ring-[var(--pz-cipher)] sm:text-sm sm:leading-6 px-4 transition-all duration-150 cursor-text disabled:opacity-50" 
                value={email} 
                onChange={e => setEmail(e.target.value)} 
                disabled={loading} 
              />
            </div>
          </div>
          
          <div>
            <label htmlFor="password-input" className="block text-sm font-medium leading-6 text-[var(--pz-text-secondary)]">{t('passwordLabel')}</label>
            <div className="mt-2 relative">
              <input 
                id="password-input" 
                type={showPassword ? "text" : "password"} 
                required 
                className="block w-full rounded-md border border-[var(--pz-border-strong)] hover:border-[var(--pz-text-muted)] focus:border-[var(--pz-cipher)] py-2.5 text-[var(--pz-text)] bg-[var(--pz-surface-inset)] shadow-sm focus:outline-none focus:ring-2 focus:ring-[var(--pz-cipher)] sm:text-sm sm:leading-6 px-4 pr-11 transition-all duration-150 cursor-text disabled:opacity-50" 
                value={password} 
                onChange={e => setPassword(e.target.value)} 
                disabled={loading} 
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 flex items-center pr-3 text-[var(--pz-text-muted)] hover:text-[var(--pz-text)] cursor-pointer disabled:cursor-not-allowed"
                aria-label="Toggle password visibility"
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>
          
          <div className="pt-2">
            <button 
              type="submit" 
              disabled={loading} 
              className="flex w-full justify-center rounded-md bg-[var(--pz-cipher)] px-4 py-2.5 text-sm font-semibold leading-6 text-[var(--pz-ink)] shadow-sm hover:bg-[var(--pz-cipher-hover)] active:scale-[0.99] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50 transition-all duration-150 cursor-pointer disabled:cursor-not-allowed"
            >
              {loading ? '...' : t('signUpButton')}
            </button>
          </div>
        </form>

        <div className="mt-8">
          <div className="relative">
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-[var(--pz-border)]" /></div>
            <div className="relative flex justify-center text-sm"><span className="bg-[var(--pz-canvas)] px-2 text-[var(--pz-text-muted)]">{t('orContinueWith')}</span></div>
          </div>

          <div className="mt-6">
            <button 
              onClick={handleGoogleSignup} 
              disabled={loading} 
              className="flex w-full justify-center items-center gap-3 rounded-md bg-[var(--pz-surface)] px-4 py-2.5 text-sm font-semibold text-[var(--pz-text)] shadow-sm border border-[var(--pz-border-strong)] hover:border-[var(--pz-text-muted)] hover:bg-[var(--pz-surface-inset)] active:scale-[0.99] transition-all duration-150 cursor-pointer disabled:cursor-not-allowed disabled:opacity-50"
            >
              <svg className="h-5 w-5" aria-hidden="true" viewBox="0 0 24 24">
                <path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z" fill="currentColor" />
              </svg>
              {t('googleButton')}
            </button>
          </div>
        </div>
        
        <p className="mt-10 text-center text-sm text-[var(--pz-text-secondary)]">
          <Link href="/login" className="font-semibold leading-6 text-[var(--pz-cipher)] hover:text-[var(--pz-cipher-hover)] transition-colors">{t('alreadyHaveAccount')}</Link>
        </p>
      </div>
    </div>
  );
}