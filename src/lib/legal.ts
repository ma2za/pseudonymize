import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { remark } from 'remark';
import html from 'remark-html';

const legalDirectory = path.join(process.cwd(), 'content', 'legal');

export type LegalDoc = {
  slug: string;
  title: string;
  lastUpdated: string;
  content: string;
  locale: string;
};

// Get full data for a specific legal doc
export async function getLegalDoc(slug: string, locale: string): Promise<LegalDoc | null> {
  const localeDir = path.join(legalDirectory, locale);
  let targetDir = localeDir;
  
  let fullPath = path.join(targetDir, `${slug}.md`);

  // Fallback to English if post doesn't exist in requested language
  if (!fs.existsSync(fullPath)) {
    targetDir = path.join(legalDirectory, 'en');
    fullPath = path.join(targetDir, `${slug}.md`);
  }

  if (!fs.existsSync(fullPath)) {
    return null; // Doc not found
  }

  const fileContents = fs.readFileSync(fullPath, 'utf8');
  const matterResult = matter(fileContents);

  const processedContent = await remark()
    .use(html)
    .process(matterResult.content);
    
  const contentHtml = processedContent.toString();

  return {
    slug,
    locale,
    title: matterResult.data.title || 'Untitled Document',
    lastUpdated: matterResult.data.lastUpdated || new Date().toISOString(),
    content: contentHtml,
  };
}