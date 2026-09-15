import createMiddleware from 'next-intl/middleware';
import {routing} from './i18n/routing';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const intlMiddleware = createMiddleware(routing);

export default function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;
  const hasSession = request.cookies.has('better-auth.session_token') || request.cookies.has('__Secure-better-auth.session_token');

  // 1. Handle legacy signout intercept
  if (pathname === '/api/auth/signout') {
    const response = NextResponse.redirect(new URL('/', request.url));
    response.cookies.delete('better-auth.session_token');
    response.cookies.delete('__Secure-better-auth.session_token');
    response.cookies.delete('better-auth.session_data');
    response.cookies.delete('__Secure-better-auth.session_data');
    response.cookies.delete('next-auth.session-token');
    response.cookies.delete('__Secure-next-auth.session-token');
    return response;
  }

  // 2. Fast Edge Route Protection to prevent unauthenticated layout flashes
  const isDashboard = /^\/([a-zA-Z-]+)\/dashboard(\/.*)?$/.test(pathname);
  if (isDashboard && !hasSession) {
    const match = pathname.match(/^\/([a-zA-Z-]+)\//);
    const locale = match ? match[1] : 'en';
    return NextResponse.redirect(new URL(`/${locale}/login`, request.url));
  }

  // 3. Redirect authenticated users away from auth pages
  const isAuthPage = /^\/([a-zA-Z-]+)\/(login|signup)(\/.*)?$/.test(pathname);
  if (isAuthPage && hasSession) {
    const match = pathname.match(/^\/([a-zA-Z-]+)\//);
    const locale = match ? match[1] : 'en';
    return NextResponse.redirect(new URL(`/${locale}/dashboard`, request.url));
  }

  // 4. Proceed with next-intl middleware
  return intlMiddleware(request);
}

export const config = {
  matcher: ['/', '/(en|es|fr|de|it|pt|nl|ru|zh|ja|ko|ar|hi|tr|pl|sv|no|da|fi|el)/:path*', '/api/auth/signout']
};