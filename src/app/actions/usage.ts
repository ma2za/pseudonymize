'use server';

import { prisma } from '@/db';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';

export async function getMonthlyUsage() {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session) {
    return { data: [], totalCredits: 0 };
  }

  // Get the date 30 days ago
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
  thirtyDaysAgo.setHours(0, 0, 0, 0);

  // Fetch usage records from the database
  const usages = await prisma.apiUsage.findMany({
    where: {
      userId: session.user.id,
      createdAt: {
        gte: thirtyDaysAgo,
      },
    },
    select: {
      createdAt: true,
      credits: true,
    },
    orderBy: {
      createdAt: 'asc',
    },
  });

  // Aggregate by day
  const dailyUsageMap = new Map<string, number>();
  let totalCredits = 0;

  // Initialize the last 30 days with 0 so the chart doesn't have missing dates
  for (let i = 29; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    // Format to YYYY-MM-DD
    const dateStr = date.toISOString().split('T')[0];
    dailyUsageMap.set(dateStr, 0);
  }

  // Populate actual data
  usages.forEach((usage) => {
    const dateStr = usage.createdAt.toISOString().split('T')[0];
    if (dailyUsageMap.has(dateStr)) {
      dailyUsageMap.set(dateStr, dailyUsageMap.get(dateStr)! + usage.credits);
      totalCredits += usage.credits;
    }
  });

  // Format for Recharts
  const data = Array.from(dailyUsageMap.entries()).map(([date, count]) => ({
    date, // YYYY-MM-DD
    displayDate: new Date(date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }),
    count,
  }));

  return { data, totalCredits };
}
