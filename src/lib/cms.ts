import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { remark } from 'remark';
import html from 'remark-html';

const contentDirectory = path.join(process.cwd(), 'content', 'blog');

export type BlogPost = {
  slug: string;
  title: string;
  date: string;
  excerpt: string;
  content: string;
  locale: string;
};

// Gets a list of all posts for a specific locale
export function getBlogPosts(locale: string): Omit<BlogPost, 'content'>[] {
  const localeDir = path.join(contentDirectory, locale);
  
  // Fallback to English if the locale directory doesn't exist yet
  const targetDir = fs.existsSync(localeDir) ? localeDir : path.join(contentDirectory, 'en');
  
  if (!fs.existsSync(targetDir)) return [];

  const fileNames = fs.readdirSync(targetDir);
  const allPostsData = fileNames
    .filter(fileName => fileName.endsWith('.md'))
    .map(fileName => {
      const slug = fileName.replace(/\.md$/, '');
      const fullPath = path.join(targetDir, fileName);
      const fileContents = fs.readFileSync(fullPath, 'utf8');

      const matterResult = matter(fileContents);

      return {
        slug,
        locale,
        title: matterResult.data.title || 'Untitled',
        date: matterResult.data.date || new Date().toISOString(),
        excerpt: matterResult.data.excerpt || '',
      };
  });

  return allPostsData.sort((a, b) => (a.date < b.date ? 1 : -1));
}

// Get full data for a specific post
export async function getBlogPost(slug: string, locale: string): Promise<BlogPost | null> {
  const localeDir = path.join(contentDirectory, locale);
  let targetDir = localeDir;
  
  let fullPath = path.join(targetDir, `${slug}.md`);

  // Fallback to English if post doesn't exist in requested language
  if (!fs.existsSync(fullPath)) {
    targetDir = path.join(contentDirectory, 'en');
    fullPath = path.join(targetDir, `${slug}.md`);
  }

  if (!fs.existsSync(fullPath)) {
    return null; // Post not found
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
    title: matterResult.data.title || 'Untitled',
    date: matterResult.data.date || new Date().toISOString(),
    excerpt: matterResult.data.excerpt || '',
    content: contentHtml,
  };
}