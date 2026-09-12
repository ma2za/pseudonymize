/* eslint-disable @typescript-eslint/no-require-imports */
const fs = require('fs');
const translate = require('google-translate-api-x');

const baseData = JSON.parse(fs.readFileSync('./messages/en.json', 'utf8'));
const locales = ['es', 'fr', 'de', 'it', 'pt', 'nl', 'ru', 'zh-CN', 'ja', 'ko', 'ar', 'hi', 'tr', 'pl', 'sv', 'no', 'da', 'fi', 'el'];

function extractStrings(obj, path = '', strings = []) {
  for (const key of Object.keys(obj)) {
    const currentPath = path ? `${path}.${key}` : key;
    if (typeof obj[key] === 'string') {
      strings.push({ path: currentPath, text: obj[key] });
    } else if (typeof obj[key] === 'object') {
      extractStrings(obj[key], currentPath, strings);
    }
  }
  return strings;
}

function setNested(obj, path, value) {
  const keys = path.split('.');
  let current = obj;
  for (let i = 0; i < keys.length - 1; i++) {
    if (!current[keys[i]]) current[keys[i]] = {};
    current = current[keys[i]];
  }
  current[keys[keys.length - 1]] = value;
}

async function run() {
  const stringEntries = extractStrings(baseData);
  // Protect variables like {credits} from translation by using a span
  const textsToTranslate = stringEntries.map(e => e.text.replace(/\{([^}]+)\}/g, '<span translate="no">{$1}</span>'));

  for (const loc of locales) {
    console.log(`Translating to ${loc}...`);
    try {
      // Batch translate all strings for this locale
      const res = await translate(textsToTranslate, { to: loc });
      const translatedObj = {};
      
      const responses = Array.isArray(res) ? res : [res]; // handle single item array fallback
      
      responses.forEach((r, idx) => {
        let cleanText = r.text;
        // Clean up any broken HTML tags added by the translator
        cleanText = cleanText.replace(/<span[^>]*>/gi, '').replace(/<\/span>/gi, '');
        // Sometimes brackets get spaces added around them
        cleanText = cleanText.replace(/\{\s+([^}]+)\s+\}/g, '{$1}');
        
        setNested(translatedObj, stringEntries[idx].path, cleanText);
      });
      
      const filename = loc === 'zh-CN' ? 'zh' : loc;
      fs.writeFileSync(`./messages/${filename}.json`, JSON.stringify(translatedObj, null, 2));
      console.log(`Success: ${filename}.json written.`);
    } catch(e) {
      console.error(`Error translating ${loc}:`, e.message);
    }
    // Respect rate limits
    await new Promise(r => setTimeout(r, 2000));
  }
}

run(); 