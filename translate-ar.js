/* eslint-disable @typescript-eslint/no-require-imports */
const fs = require('fs');
const translate = require('google-translate-api-x');

const baseData = JSON.parse(fs.readFileSync('./messages/en.json', 'utf8'));
const locales = ['ar'];

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
  const textsToTranslate = stringEntries.map(e => e.text.replace(/\{([^}]+)\}/g, '<span translate="no">{$1}</span>'));

  for (const loc of locales) {
    console.log(`Translating to ${loc}...`);
    try {
      const res = await translate(textsToTranslate, { to: loc });
      const translatedObj = {};
      
      const responses = Array.isArray(res) ? res : [res];
      
      responses.forEach((r, idx) => {
        let cleanText = r.text;
        cleanText = cleanText.replace(/<span[^>]*>/gi, '').replace(/<\/span>/gi, '');
        cleanText = cleanText.replace(/\{\s+([^}]+)\s+\}/g, '{$1}');
        
        setNested(translatedObj, stringEntries[idx].path, cleanText);
      });
      
      fs.writeFileSync(`./messages/${loc}.json`, JSON.stringify(translatedObj, null, 2));
      console.log(`Success: ${loc}.json written.`);
    } catch(e) {
      console.error(`Error translating ${loc}:`, e.message);
    }
  }
}

run(); 