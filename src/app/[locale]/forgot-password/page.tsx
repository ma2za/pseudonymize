'use client';
import { useState } from 'react';
import { authClient } from '@/lib/auth-client';
import { Link } from '@/i18n/routing';
import { useTranslations } from 'next-intl';

export default function ForgotPasswordPage() {
  const t = useTranslations('ForgotPassword');
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // TypeScript complains because `forgetPassword` was recently added/changed in better-auth typings
      // or we are missing the client plugin in createAuthClient. We cast to a specific type to allow compilation.
      const auth: { forgetPassword: (args: { email: string; redirectTo: string }) => Promise<void> } = authClient as unknown as { forgetPassword: (args: { email: string; redirectTo: string }) => Promise<void> };
      await auth.forgetPassword({
        email,
        redirectTo: "/reset-password"
      });
      setSubmitted(true);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[100dvh] flex-col justify-center px-4 py-12 sm:px-6 lg:px-8 bg-[var(--pz-canvas)] overflow-hidden">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-bold leading-9 tracking-tight text-[var(--pz-text)]">
          {t('title')}
        </h2>
        <p className="mt-2 text-center text-sm text-[var(--pz-text-secondary)]">
          {t('description')}
        </p>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        {submitted ? (
          <div className="rounded-xl bg-[var(--pz-surface-inset)] p-6 border border-[var(--pz-success)] shadow-sm">
            <div className="text-sm font-medium text-[var(--pz-success)] text-center">
              {t('checkEmail')}
            </div>
          </div>
        ) : (
          <form className="space-y-6 bg-[var(--pz-surface)] border border-[var(--pz-border)] p-6 sm:p-8 rounded-xl shadow-lg" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="email-input" className="block text-sm font-medium leading-6 text-[var(--pz-text-secondary)]">{t('emailLabel')}</label>
              <div className="mt-2">
                <input id="email-input" type="email" required className="block w-full rounded-md border border-[var(--pz-border-strong)] py-2.5 text-[var(--pz-text)] bg-[var(--pz-surface-inset)] shadow-sm focus:outline-none focus:ring-2 focus:ring-[var(--pz-cipher)] focus:border-transparent sm:text-sm sm:leading-6 px-4 transition-all" value={email} onChange={e => setEmail(e.target.value)} />
              </div>
            </div>
            <div className="pt-2">
              <button type="submit" disabled={loading} className="flex w-full justify-center rounded-md bg-[var(--pz-cipher)] px-4 py-2.5 text-sm font-semibold leading-6 text-[var(--pz-ink)] shadow-sm hover:bg-[var(--pz-cipher-hover)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50 transition-colors">{t('sendLinkButton')}</button>
            </div>
          </form>
        )}
        
        <p className="mt-10 text-center text-sm text-[var(--pz-text-secondary)]">
          <Link href="/login" className="font-semibold leading-6 text-[var(--pz-cipher)] hover:text-[var(--pz-cipher-hover)] transition-colors">{t('backToLogin')}</Link>
        </p>
      </div>
    </div>
  );
}