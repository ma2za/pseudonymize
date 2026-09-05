import { getTranslations, setRequestLocale } from 'next-intl/server';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';
import { ProfileForm, DeleteAccount } from '@/components/SettingsForms';
import { Link } from '@/i18n/routing';

export default async function SettingsPage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Dashboard');

  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session) {
    redirect(`/${locale}/login`);
  }

  const dict = {
    nameLabel: t('nameLabel'),
    emailLabel: t('emailLabel'),
    saveChanges: t('saveChanges'),
    saving: t('saving'),
    profileUpdated: t('profileUpdated'),
    dangerZone: t('dangerZone'),
    deleteWarning: t('deleteWarning'),
    deleteAccountBtn: t('deleteAccountBtn'),
    deleting: t('deleting'),
    confirmDelete: t('confirmDelete'),
  };

  return (
    <div className="bg-[var(--pz-canvas)] flex flex-col">
      <main className="flex-1 max-w-3xl w-full mx-auto py-6 sm:py-10 px-4 sm:px-6 lg:px-8 space-y-6 sm:space-y-8">
        
        <div className="mb-4">
          <Link href="/dashboard" className="text-sm font-semibold leading-6 text-[var(--pz-cipher-strong)] hover:text-[var(--pz-cipher)]">
            ← {t('backToDashboard')}
          </Link>
        </div>

        <div className="bg-[var(--pz-surface)] overflow-hidden shadow-sm rounded-lg border border-[var(--pz-border)]">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-[var(--pz-text)]">
              {t('profileSettingsTitle')}
            </h3>
            <div className="mt-2 max-w-xl text-sm text-[var(--pz-text-secondary)] mb-6">
              <p>{t('profileSettingsDesc')}</p>
            </div>
            
            <ProfileForm initialName={session.user.name} initialEmail={session.user.email} dict={dict} />
            
            <DeleteAccount dict={dict} />
            
          </div>
        </div>
      </main>
    </div>
  );
}