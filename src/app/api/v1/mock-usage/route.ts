import { NextResponse } from 'next/server';
import { prisma } from '@/db';
import { nanoid } from 'nanoid';

export async function POST(req: Request) {
  try {
    const { userId } = await req.json();
    
    if (!userId) {
      return NextResponse.json({ error: 'Missing userId' }, { status: 400 });
    }
    
    const usageRecords = [];
    
    // Seed 100 random usages over the past 30 days
    for (let i = 0; i < 100; i++) {
      const daysAgo = Math.floor(Math.random() * 30);
      const randomDate = new Date();
      randomDate.setDate(randomDate.getDate() - daysAgo);
      
      usageRecords.push({
        id: nanoid(16),
        userId,
        endpoint: Math.random() > 0.5 ? '/v1/text' : '/v1/data',
        credits: Math.floor(Math.random() * 5) + 1,
        createdAt: randomDate
      });
    }
    
    await prisma.apiUsage.createMany({
      data: usageRecords
    });
    
    return NextResponse.json({ success: true, inserted: usageRecords.length });
  } catch (error) {
    return NextResponse.json({ error: String(error) }, { status: 500 });
  }
}
