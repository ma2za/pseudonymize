/* eslint-disable @typescript-eslint/no-require-imports */
const fs = require('fs');
const path = require('path');
const { GoogleGenAI } = require('@google/genai');

const ai = new GoogleGenAI();
const messagesDir = path.join(__dirname, 'messages');
const baseFile = path.join(messagesDir, 'en.json');
const baseData = JSON.parse(fs.readFileSync(baseFile, 'utf8'));

const locales = ['es', 'fr', 'de', 'it', 'pt', 'nl', 'ru', 'zh', 'ja', 'ko', 'ar', 'hi', 'tr', 'pl', 'sv', 'no', 'da', 'fi', 'el'];

async function translate() {
  for (const locale of locales) {
    console.log(`Translating to ${locale}...`);
    try {
      const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: `You are an expert translator. Translate the following JSON dictionary to the ${locale} locale. Ensure that variables inside brackets like {credits} remain exactly as they are. Return ONLY valid JSON, nothing else.

        ${JSON.stringify(baseData, null, 2)}`
      });

      let text = response.text;
      
      // Clean markdown formatting if present
      if (text.startsWith('\`\`\`json')) {
        text = text.replace(/^\`\`\`json\n/, '').replace(/\n\`\`\`$/, '');
      }
      
      const translatedJson = JSON.parse(text);
      fs.writeFileSync(path.join(messagesDir, `${locale}.json`), JSON.stringify(translatedJson, null, 2));
      console.log(`Successfully translated to ${locale}.`);
    } catch (e) {
      console.error(`Failed to translate ${locale}:`, e.message);
    }
  }
}

translate(); 