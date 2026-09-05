'use server';

import { db } from '@/db';
import { apiKey } from '@/db/schema';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { nanoid } from 'nanoid';
import { eq, and } from 'drizzle-orm';
import { revalidatePath } from 'next/cache';

export async function createApiKey(name: string) {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session) {
    throw new Error("Unauthorized");
  }

  // Generate a key prefix for visual identification + random string
  const rawKey = `ps_live_${nanoid(32)}`;

  await db.insert(apiKey).values({
    id: nanoid(16),
    userId: session.user.id,
    name: name || "Default Key",
    key: rawKey,
  });

  revalidatePath('/[locale]/dashboard', 'page');
  return { success: true, key: rawKey };
}

export async function getApiKeys() {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session) return [];

  const keys = await db.select({
    id: apiKey.id,
    name: apiKey.name,
    key: apiKey.key,
    createdAt: apiKey.createdAt,
    lastUsedAt: apiKey.lastUsedAt,
    isActive: apiKey.isActive,
  }).from(apiKey).where(eq(apiKey.userId, session.user.id));

  // Mask keys before sending to client for display (except for the first generation)
  return keys.map(k => ({
    ...k,
    // Only show first 12 chars of the live key, mask the rest
    maskedKey: `${k.key.substring(0, 12)}${'*'.repeat(16)}`,
  }));
}

export async function revokeApiKey(id: string) {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session) {
    throw new Error("Unauthorized");
  }

  await db.delete(apiKey).where(
    and(
      eq(apiKey.id, id),
      eq(apiKey.userId, session.user.id)
    )
  );

  revalidatePath('/[locale]/dashboard', 'page');
  return { success: true };
}