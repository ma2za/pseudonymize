'use server';

import { auth } from '@/lib/auth';
import { prisma } from '@/db';
import { headers } from 'next/headers';
import { revalidatePath } from 'next/cache';

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
    await prisma.user.update({
      where: { id: session.user.id },
      data: { name, email }
    });
      
    revalidatePath('/[locale]/dashboard/settings', 'page');
    return { success: true };
  } catch (error) {
    console.error('Failed to update profile:', error);
    return { error: error instanceof Error ? error.message : 'Failed to update profile' };
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
    // Due to the schema having cascade rules, deleting the user should drop sessions, accounts, and keys.
    // We execute in a transaction or manually delete to be safe.
    await prisma.$transaction([
      prisma.apiKey.deleteMany({ where: { userId } }),
      prisma.session.deleteMany({ where: { userId } }),
      prisma.account.deleteMany({ where: { userId } }),
      prisma.user.delete({ where: { id: userId } })
    ]);

    return { success: true };
  } catch (error) {
    console.error('Failed to delete account:', error);
    return { error: 'An error occurred while deleting your account.' };
  }
}