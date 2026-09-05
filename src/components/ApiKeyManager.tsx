'use client';

import { useState } from 'react';
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
          className="flex-1 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 px-3"
        />
        <button 
          onClick={handleCreate} 
          disabled={loading}
          className="inline-flex justify-center items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {loading ? dict.creating : dict.createNewKey}
        </button>
      </div>

      {newKey && (
        <div className="mt-4 p-4 bg-green-50 rounded-md border border-green-200">
          <p className="text-sm font-medium text-green-800 mb-2">{dict.keyGeneratedWarning}</p>
          <div className="flex items-center gap-2">
            <code className="flex-1 bg-white px-3 py-2 rounded border border-green-300 text-sm font-mono break-all">{newKey}</code>
            <button onClick={copyToClipboard} className="p-2 bg-white rounded border border-green-300 hover:bg-green-50 text-green-700">
              {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
            </button>
          </div>
        </div>
      )}

      <div className="mt-8 border-t border-gray-200 pt-6">
        <h4 className="text-md font-medium text-gray-900">{dict.yourKeysTitle}</h4>
        
        {keys.length === 0 ? (
          <p className="text-sm text-gray-500 mt-4">{dict.noKeysYet}</p>
        ) : (
          <ul className="mt-4 divide-y divide-gray-200">
            {keys.map((k) => (
              <li key={k.id} className="py-4 flex justify-between items-center">
                <div>
                  <p className="text-sm font-medium text-gray-900">{k.name}</p>
                  <p className="text-sm font-mono text-gray-500 mt-1">{k.maskedKey}</p>
                  <p className="text-xs text-gray-400 mt-1">
                    {dict.created}: {new Date(k.createdAt).toLocaleDateString()}
                  </p>
                </div>
                <button
                  onClick={() => handleRevoke(k.id)}
                  className="text-red-600 hover:text-red-800 p-2"
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