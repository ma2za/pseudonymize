require('dotenv').config({ path: '.env.local' });
const { drizzle } = require('drizzle-orm/node-postgres');
const { migrate } = require('drizzle-orm/node-postgres/migrator');
const { Pool } = require('pg');
const path = require('path');

async function run() {
  if (!process.env.DATABASE_URL) {
    console.warn('DATABASE_URL is not set. Skipping migrations.');
    return;
  }

  console.log('Connecting to database to run migrations...');
  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
  });
  
  const db = drizzle(pool);
  
  console.log('Running migrations from /drizzle folder...');
  await migrate(db, { migrationsFolder: path.join(__dirname, '../drizzle') });
  
  console.log('Migrations complete!');
  await pool.end();
}

run().catch((err) => {
  console.error('Migration failed!', err);
  process.exit(1);
});