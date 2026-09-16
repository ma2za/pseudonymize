import createMiddleware from 'next-intl/middleware';
import {routing} from './i18n/routing';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const intlMiddleware = createMiddleware(routing);

export default function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;
  const hasSession = request.cookies.has('better-auth.session_token') || request.cookies.has('__Secure-better-auth.session_token');

  // 2. Fast Edge Route Protection to prevent unauthenticated layout flashes
  const isDashboard = /^\/([a-zA-Z-]+)\/dashboard(\/.*)?$/.test(pathname);
  if (isDashboard && !hasSession) {
    const match = pathname.match(/^\/([a-zA-Z-]+)\//);
    const locale = match ? match[1] : 'en';
    return NextResponse.redirect(new URL(`/${locale}/login`, request.url));
  }

  // 4. Proceed with next-intl middleware
  return intlMiddleware(request);
}

export const config = {
  matcher: ['/', '/(en|es|fr|de|it|pt|nl|ru|zh|ja|ko|ar|hi|tr|pl|sv|no|da|fi|el)/:path*', '/api/auth/signout']  
};