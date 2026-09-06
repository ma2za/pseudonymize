const fs = require('fs');
const path = require('path');

const baseData = JSON.parse(fs.readFileSync('./messages/en.json', 'utf8'));
const locales = ['ar', 'da', 'de', 'el', 'es', 'fi', 'fr', 'hi', 'it', 'ja', 'ko', 'nl', 'no', 'pl', 'pt', 'ru', 'sv', 'tr', 'zh'];

function syncKeys(base, target) {
  let updated = false;
  for (const key in base) {
    if (typeof base[key] === 'object' && base[key] !== null) {
      if (!target[key] || typeof target[key] !== 'object') {
        target[key] = {};
        updated = true;
      }
      if (syncKeys(base[key], target[key])) updated = true;
    } else {
      if (target[key] === undefined) {
        target[key] = base[key];
        updated = true;
      }
    }
  }
  
  // Optional: remove keys that don't exist in base
  for (const key in target) {
    if (base[key] === undefined) {
       delete target[key];
       updated = true;
    } else if (typeof target[key] === 'object' && typeof base[key] === 'object') {
       // Deep cleanup is handled well enough for now
    }
  }
  
  return updated;
}

for (const loc of locales) {
  const file = `./messages/${loc}.json`;
  let targetData = {};
  if (fs.existsSync(file)) {
    targetData = JSON.parse(fs.readFileSync(file, 'utf8'));
  }
  const updated = syncKeys(baseData, targetData);
  if (updated) {
    fs.writeFileSync(file, JSON.stringify(targetData, null, 2));
    console.log(`Synced ${loc}.json`);
  }
}
