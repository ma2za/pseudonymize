'use server';

import { auth } from '@/lib/auth';
import { db } from '@/db';
import { user, session as sessionTable, account, apiKey } from '@/db/schema';
import { eq } from 'drizzle-orm';
import { headers } from 'next/headers';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function updateProfile(formData: FormData) {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session) {
    throw new Error('Unauthorized');
  }

  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  if (!name || !email) {
    return { error: 'Name and email are required' };
  }

  try {
    await db.update(user)
      .set({ name, email })
      .where(eq(user.id, session.user.id));
      
    revalidatePath('/[locale]/dashboard/settings', 'page');
    return { success: true };
  } catch (error: any) {
    console.error('Failed to update profile:', error);
    return { error: error.message || 'Failed to update profile' };
  }
}

export async function deleteAccount() {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session) {
    throw new Error('Unauthorized');
  }

  const userId = session.user.id;

  try {
    // Due to the schema having cascade rules, deleting the user should ideally drop sessions, accounts, and keys.
    // However, it's safer to explicitly execute them if cascade wasn't perfectly configured at the database level.
    await db.delete(apiKey).where(eq(apiKey.userId, userId));
    await db.delete(sessionTable).where(eq(sessionTable.userId, userId));
    await db.delete(account).where(eq(account.userId, userId));
    await db.delete(user).where(eq(user.id, userId));

    return { success: true };
  } catch (error: any) {
    console.error('Failed to delete account:', error);
    return { error: 'An error occurred while deleting your account.' };
  }
}