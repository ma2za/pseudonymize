import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Shield } from 'lucide-react';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';
import ApiKeyManager from '@/components/ApiKeyManager';
import CreditPurchase from '@/components/CreditPurchase';
import { getApiKeys } from '@/app/actions/api-keys';

export default async function DashboardPage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Dashboard');

  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session) {
    redirect(`/${locale}/login`);
  }

  const initialKeys = await getApiKeys();

  // Assuming credit balance is stored in the DB
  const credits = (session.user as any).credits || 0;

  const keyDict = {
    keyNamePlaceholder: t('keyNamePlaceholder'),
    defaultKeyName: t('defaultKeyName'),
    creating: t('creating'),
    createNewKey: t('createNewKey'),
    keyGeneratedWarning: t('keyGeneratedWarning'),
    yourKeysTitle: t('yourKeysTitle'),
    noKeysYet: t('noKeysYet'),
    created: t('created'),
    revokeKey: t('revokeKey')
  };

  const purchaseDict = {
    package10k: t('package10k'),
    package50k: t('package50k'),
    mostPopular: t('mostPopular'),
    creditsLabel: t('creditsLabel'),
    buyCredits: t('buyCredits'),
    redirecting: t('redirecting')
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Shield className="w-8 h-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-900 hidden sm:block">{t('brandName')}</span>
            </div>
            <div className="flex items-center">
              <span className="text-sm text-gray-700 mr-4 truncate max-w-[120px] sm:max-w-xs">{session.user.email}</span>
              <form action="/api/auth/signout" method="POST">
                <button type="submit" className="text-sm font-semibold text-gray-900 hover:text-blue-600 whitespace-nowrap">
                  {t('signOut')}
                </button>
              </form>
            </div>
          </div>
        </div>
      </nav>

      <main className="flex-1 max-w-7xl w-full mx-auto py-6 sm:py-10 px-4 sm:px-6 lg:px-8 space-y-6 sm:space-y-8">
        <div className="bg-white overflow-hidden shadow rounded-lg border border-gray-200">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              {t('apiKeysTitle')}
            </h3>
            <div className="mt-2 max-w-xl text-sm text-gray-500 mb-5">
              <p>{t('apiKeysDescription')}</p>
            </div>
            
            <ApiKeyManager initialKeys={initialKeys} dict={keyDict} />
            
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg border border-gray-200">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              {t('billingTitle')}
            </h3>
            <div className="mt-2 max-w-xl text-sm text-gray-500">
              <p>{t('creditsRemaining', { credits })}</p>
            </div>
            
            <CreditPurchase dict={purchaseDict} />
            
          </div>
        </div>
      </main>
    </div>
  );
}