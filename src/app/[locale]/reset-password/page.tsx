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
    <div className="flex min-h-[100dvh] flex-col justify-center px-4 py-12 sm:px-6 lg:px-8 bg-gray-50 overflow-hidden">
      <div className="sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 className="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
          {t('title')}
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-sm">
        {success ? (
          <div className="rounded-md bg-green-50 p-4 border border-green-200">
            <div className="text-sm font-medium text-green-800 text-center">
              {t('successMessage')}
            </div>
          </div>
        ) : (
          <form className="space-y-6" onSubmit={handleReset}>
            <div>
              <label htmlFor="password-input" className="block text-sm font-medium leading-6 text-gray-900">{t('passwordLabel')}</label>
              <div className="mt-2">
                <input id="password-input" type="password" required className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 px-3" value={password} onChange={e => setPassword(e.target.value)} />
              </div>
            </div>
            <div>
              <button type="submit" disabled={loading} className="flex w-full justify-center rounded-md bg-blue-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-blue-500 disabled:opacity-50">{t('resetButton')}</button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}