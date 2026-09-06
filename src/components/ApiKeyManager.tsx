'use client';

import { useState, useEffect } from 'react';
import { createApiKey, revokeApiKey } from '@/app/actions/api-keys';
import { Trash2, Copy, Check } from 'lucide-react';

type ApiKey = {
  id: string;
  name: string | null;
  key: string;
  maskedKey: string;
  createdAt: Date;
  lastUsedAt: Date | null;
  isActive: boolean;
};

export default function ApiKeyManager({ initialKeys, dict }: { initialKeys: ApiKey[], dict: any }) {
  const [keys, setKeys] = useState<ApiKey[]>(initialKeys);
  const [loading, setLoading] = useState(false);
  const [newKey, setNewKey] = useState<string | null>(null);
  const [keyName, setKeyName] = useState('');
  const [copied, setCopied] = useState(false);
  const [autoCreated, setAutoCreated] = useState(false);

  useEffect(() => {
    if (initialKeys.length === 0 && !loading && !newKey && !autoCreated) {
      setAutoCreated(true);
      handleCreate();
    }
  }, [initialKeys, loading, newKey, autoCreated]);

  const handleCreate = async () => {
    setLoading(true);
    try {
      const res = await createApiKey(keyName || dict.defaultKeyName);
      if (res.success) {
        setNewKey(res.key);
        // Optimistically update list (we'll fetch actual later or rely on revalidatePath)
        setKeys([{
          id: 'temp',
          name: keyName || dict.defaultKeyName,
          key: res.key,
          maskedKey: `${res.key.substring(0, 12)}${'*'.repeat(16)}`,
          createdAt: new Date(),
          lastUsedAt: null,
          isActive: true
        }, ...keys]);
        setKeyName('');
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleRevoke = async (id: string) => {
    try {
      const res = await revokeApiKey(id);
      if (res.success) {
        setKeys(keys.filter(k => k.id !== id));
      }
    } catch (e) {
      console.error(e);
    }
  };

  const copyToClipboard = () => {
    if (newKey) {
      navigator.clipboard.writeText(newKey);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div>
      <div className="flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          placeholder={dict.keyNamePlaceholder}
          value={keyName}
          onChange={(e) => setKeyName(e.target.value)}
          className="flex-1 rounded-md border border-[var(--pz-border-strong)] py-2 text-[var(--pz-text)] bg-[var(--pz-surface-inset)] shadow-sm focus:ring-2 focus:ring-[var(--pz-cipher)] sm:text-sm sm:leading-6 px-3"
        />
        <button 
          onClick={handleCreate} 
          disabled={loading}
          className="inline-flex justify-center items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-[var(--pz-ink)] bg-[var(--pz-cipher)] hover:bg-[var(--pz-cipher-hover)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--pz-cipher)] disabled:opacity-50"
        >
          {loading ? dict.creating : dict.createNewKey}
        </button>
      </div>

      {newKey && (
        <div className="mt-6">
          <div className="p-4 bg-[var(--pz-canvas)] rounded-md border border-[var(--pz-border-strong)] mb-6 shadow-sm">
            <p className="text-sm font-medium text-[var(--pz-text)] mb-3">{dict.keyGeneratedWarning}</p>
            <div className="flex items-center gap-2">
              <code className="flex-1 bg-[var(--pz-surface-inset)] px-3 py-2 rounded border border-[var(--pz-border)] text-sm font-mono break-all text-[var(--pz-text)]">{newKey}</code>
              <button onClick={copyToClipboard} className="p-2 bg-[var(--pz-surface)] rounded border border-[var(--pz-border)] hover:bg-[var(--pz-surface-inset)] text-[var(--pz-text)] transition-colors">
                {copied ? <Check className="w-4 h-4 text-[var(--pz-cipher-strong)]" /> : <Copy className="w-4 h-4" />}
              </button>
            </div>
          </div>
          
          <div className="bg-[#050A0F] border border-[#172630] rounded-xl p-6 font-mono text-sm text-[#758690] overflow-x-auto shadow-2xl relative">
            <div className="absolute top-4 right-4 uppercase text-xs tracking-widest text-[#48D6B0] border border-[#48D6B0] rounded px-2 py-1 bg-[#050A0F]">Quickstart</div>
            <span className="text-[#A6B5BD]">curl</span> https://api.pseudonymize.io/v1/text \<br/>
            &nbsp;&nbsp;-H <span className="text-[#78AFFF]">"Authorization: Bearer {newKey}"</span> \<br/>
            &nbsp;&nbsp;-H <span className="text-[#78AFFF]">"Content-Type: application/json"</span> \<br/>
            &nbsp;&nbsp;-d '&#123;<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#78AFFF]">"text"</span>: <span className="text-[#48D6B0]">"Alice lives in Munich"</span>,<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#78AFFF]">"policy"</span>: <span className="text-[#48D6B0]">"default"</span><br/>
            &nbsp;&nbsp;&#125;'
          </div>
        </div>
      )}

      <div className="mt-8 border-t border-[var(--pz-border)] pt-6">
        <h4 className="text-md font-medium text-[var(--pz-text)]">{dict.yourKeysTitle}</h4>
        
        {keys.length === 0 ? (
          <p className="text-sm text-[var(--pz-text-secondary)] mt-4">{dict.noKeysYet}</p>
        ) : (
          <ul className="mt-4 divide-y divide-[var(--pz-border)]">
            {keys.map((k) => (
              <li key={k.id} className="py-4 flex justify-between items-center">
                <div>
                  <p className="text-sm font-medium text-[var(--pz-text)]">{k.name}</p>
                  <p className="text-sm font-mono text-[var(--pz-text-secondary)] mt-1">{k.maskedKey}</p>
                  <p className="text-xs text-[var(--pz-text-muted)] mt-1">
                    {dict.created}: {new Date(k.createdAt).toLocaleDateString()}
                  </p>
                </div>
                <button
                  onClick={() => handleRevoke(k.id)}
                  className="text-red-600 hover:text-red-800 p-2 transition-colors"
                  title={dict.revokeKey}
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}