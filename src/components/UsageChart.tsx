'use client';

import { useMemo } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

type UsageData = {
  date: string;
  displayDate: string;
  count: number;
};

export default function UsageChart({ data = [], dict }: { data: UsageData[], dict: Record<string, string> }) {
  const isDataEmpty = useMemo(() => {
    if (!data || data.length === 0) return true;
    return data.every(d => d.count === 0);
  }, [data]);

  return (
    <div className="w-full h-64 mt-4" suppressHydrationWarning>
      {isDataEmpty ? (
        <div className="w-full h-full flex items-center justify-center border border-dashed border-[var(--pz-border-strong)] rounded-md bg-[var(--pz-surface-inset)]">
          <p className="text-sm text-[var(--pz-text-muted)]">{dict.noUsageData || "No API usage recorded in the last 30 days."}</p>
        </div>
      ) : (
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--pz-cipher)" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="var(--pz-cipher)" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--pz-border)" />
            <XAxis 
              dataKey="displayDate" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fontSize: 12, fill: 'var(--pz-text-muted)' }} 
              minTickGap={30}
            />
            <YAxis 
              axisLine={false} 
              tickLine={false} 
              tick={{ fontSize: 12, fill: 'var(--pz-text-muted)' }} 
              allowDecimals={false}
            />
            <Tooltip 
              contentStyle={{ backgroundColor: 'var(--pz-surface-raised)', border: '1px solid var(--pz-border)', borderRadius: '6px', color: 'var(--pz-text)' }}
              itemStyle={{ color: 'var(--pz-cipher-strong)' }}
              labelStyle={{ color: 'var(--pz-text-secondary)', marginBottom: '4px' }}
              cursor={{ stroke: 'var(--pz-border-strong)', strokeWidth: 1, strokeDasharray: '3 3' }}
            />
            <Area 
              type="monotone" 
              dataKey="count" 
              name={dict.creditsUsed || "Credits Used"} 
              stroke="var(--pz-cipher)" 
              strokeWidth={2}
              fillOpacity={1} 
              fill="url(#colorCount)" 
              isAnimationActive={false} // Disable animation for e2e stability
            />
          </AreaChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
