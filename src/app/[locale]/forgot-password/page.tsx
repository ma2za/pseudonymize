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
      await authClient.forgetPassword({
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
    <div className="flex min-h-[100dvh] flex-col justify-center px-4 py-12 sm:px-6 lg:px-8 bg-gray-50 overflow-hidden">
      <div className="sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 className="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
          {t('title')}
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          {t('description')}
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-sm">
        {submitted ? (
          <div className="rounded-md bg-green-50 p-4 border border-green-200">
            <div className="text-sm font-medium text-green-800 text-center">
              {t('checkEmail')}
            </div>
          </div>
        ) : (
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="email-input" className="block text-sm font-medium leading-6 text-gray-900">{t('emailLabel')}</label>
              <div className="mt-2">
                <input id="email-input" type="email" required className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 px-3" value={email} onChange={e => setEmail(e.target.value)} />
              </div>
            </div>
            <div>
              <button type="submit" disabled={loading} className="flex w-full justify-center rounded-md bg-blue-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-blue-500 disabled:opacity-50">{t('sendLinkButton')}</button>
            </div>
          </form>
        )}
        
        <p className="mt-10 text-center text-sm text-gray-500">
          <Link href="/login" className="font-semibold leading-6 text-blue-600 hover:text-blue-500">{t('backToLogin')}</Link>
        </p>
      </div>
    </div>
  );
}