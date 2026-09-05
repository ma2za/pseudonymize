import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as schema from './schema';
import * as dotenv from 'dotenv';

// Explicitly load .env.local for script environments (like Playwright teardown) that don't go through Next.js
dotenv.config({ path: '.env.local' });

// In Docker build environments, the DB might be unreachable. 
// Drizzle/pg will fail aggressively if it tries to eagerly connect.
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgres://dummy:dummy@localhost:5432/dummy',
});

// We catch eager connection errors to prevent build crashes
pool.on('error', (err) => {
  console.warn('PostgreSQL Pool Error (Safe to ignore during build):', err.message);
});

export const db = drizzle(pool, { schema });