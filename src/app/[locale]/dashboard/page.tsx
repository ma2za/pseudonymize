import { getTranslations, setRequestLocale } from 'next-intl/server';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';
import ApiKeyManager from '@/components/ApiKeyManager';
import CreditPurchase from '@/components/CreditPurchase';
import { getApiKeys } from '@/app/actions/api-keys';
import Image from 'next/image';
import { Link } from '@/i18n/routing';

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
    <div className="bg-gray-50 flex flex-col">
      <main className="flex-1 max-w-7xl w-full mx-auto py-6 sm:py-10 px-4 sm:px-6 lg:px-8 space-y-6 sm:space-y-8">
        <div className="bg-white overflow-hidden shadow rounded-lg border border-gray-200">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-[var(--pz-text)]">
              {t('apiKeysTitle')}
            </h3>
            <div className="mt-2 max-w-xl text-sm text-[var(--pz-text-secondary)] mb-5">
              <p>{t('apiKeysDescription')}</p>
            </div>
            
            <div className="mb-6">
              <Link href="/dashboard/settings" className="text-sm font-semibold text-[var(--pz-cipher-strong)] hover:text-[var(--pz-cipher)]">
                {t.has('settingsLink') ? t('settingsLink') : 'Account Settings'} &rarr;
              </Link>
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