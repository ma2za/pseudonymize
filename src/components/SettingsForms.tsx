'use client';

import { useState } from 'react';
import { updateProfile, deleteAccount } from '@/app/actions/settings';
import { useRouter } from '@/i18n/routing';

export function ProfileForm({ initialName, initialEmail, dict }: { initialName: string, initialEmail: string, dict: any }) {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);
    
    const formData = new FormData(e.currentTarget);
    const res = await updateProfile(formData);
    
    if (res.error) {
      setError(res.error);
    } else {
      setSuccess(true);
    }
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && <div className="text-sm font-medium text-[var(--pz-danger)] bg-red-50 p-3 rounded-md">{error}</div>}
      {success && <div className="text-sm font-medium text-[var(--pz-success)] bg-green-50 p-3 rounded-md">{dict.profileUpdated}</div>}
      
      <div>
        <label htmlFor="name" className="block text-sm font-medium leading-6 text-[var(--pz-text)]">{dict.nameLabel}</label>
        <div className="mt-2">
          <input
            type="text"
            name="name"
            id="name"
            defaultValue={initialName}
            required
            className="block w-full rounded-md border-0 py-1.5 text-[var(--pz-ink)] shadow-sm ring-1 ring-inset ring-[var(--pz-border-strong)] focus:ring-2 focus:ring-inset focus:ring-[var(--pz-cipher)] sm:text-sm sm:leading-6 px-3"
          />
        </div>
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium leading-6 text-[var(--pz-text)]">{dict.emailLabel}</label>
        <div className="mt-2">
          <input
            type="email"
            name="email"
            id="email"
            defaultValue={initialEmail}
            required
            className="block w-full rounded-md border-0 py-1.5 text-[var(--pz-ink)] shadow-sm ring-1 ring-inset ring-[var(--pz-border-strong)] focus:ring-2 focus:ring-inset focus:ring-[var(--pz-cipher)] sm:text-sm sm:leading-6 px-3"
          />
        </div>
      </div>

      <div>
        <button
          type="submit"
          disabled={loading}
          className="inline-flex justify-center rounded-md bg-[var(--pz-cipher)] px-3 py-2 text-sm font-semibold text-[var(--pz-ink)] shadow-sm hover:bg-[var(--pz-cipher-hover)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50"
        >
          {loading ? dict.saving : dict.saveChanges}
        </button>
      </div>
    </form>
  );
}

export function DeleteAccount({ dict }: { dict: any }) {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleDelete = async () => {
    if (!window.confirm(dict.confirmDelete)) {
      return;
    }

    setLoading(true);
    const res = await deleteAccount();
    if (res.success) {
      router.push('/');
    } else {
      alert(res.error || 'Failed to delete account');
      setLoading(false);
    }
  };

  return (
    <div className="mt-8 border-t border-[var(--pz-border)] pt-8">
      <h3 className="text-base font-semibold leading-6 text-[var(--pz-danger)]">{dict.dangerZone}</h3>
      <div className="mt-2 max-w-xl text-sm text-[var(--pz-text-secondary)]">
        <p>{dict.deleteWarning}</p>
      </div>
      <div className="mt-5">
        <button
          type="button"
          onClick={handleDelete}
          disabled={loading}
          className="inline-flex items-center rounded-md bg-[var(--pz-danger)] px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50"
        >
          {loading ? dict.deleting : dict.deleteAccountBtn}
        </button>
      </div>
    </div>
  );
}