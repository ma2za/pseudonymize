'use client';
import { useState } from 'react';
import { authClient } from '@/lib/auth-client';
import { useRouter } from '@/i18n/routing';
import { useTranslations } from 'next-intl';

export default function ResetPasswordPage() {
  const t = useTranslations('ResetPassword');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const router = useRouter();

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await authClient.resetPassword({
        newPassword: password,
      });
      setSuccess(true);
      setTimeout(() => {
        router.push('/login');
      }, 2000);
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
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        {success ? (
          <div className="rounded-xl bg-[var(--pz-surface-inset)] p-6 border border-[var(--pz-success)] shadow-sm">
            <div className="text-sm font-medium text-[var(--pz-success)] text-center">
              {t('successMessage')}
            </div>
          </div>
        ) : (
          <form className="space-y-6 bg-[var(--pz-surface)] border border-[var(--pz-border)] p-6 sm:p-8 rounded-xl shadow-lg" onSubmit={handleReset}>
            <div>
              <label htmlFor="password-input" className="block text-sm font-medium leading-6 text-[var(--pz-text-secondary)]">{t('passwordLabel')}</label>
              <div className="mt-2">
                <input id="password-input" type="password" required className="block w-full rounded-md border border-[var(--pz-border-strong)] py-2.5 text-[var(--pz-text)] bg-[var(--pz-surface-inset)] shadow-sm focus:outline-none focus:ring-2 focus:ring-[var(--pz-cipher)] focus:border-transparent sm:text-sm sm:leading-6 px-4 transition-all" value={password} onChange={e => setPassword(e.target.value)} />
              </div>
            </div>
            <div className="pt-2">
              <button type="submit" disabled={loading} className="flex w-full justify-center rounded-md bg-[var(--pz-cipher)] px-4 py-2.5 text-sm font-semibold leading-6 text-[var(--pz-ink)] shadow-sm hover:bg-[var(--pz-cipher-hover)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50 transition-colors">{t('resetButton')}</button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}