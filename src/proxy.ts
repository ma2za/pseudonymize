import createMiddleware from 'next-intl/middleware';
import {routing} from './i18n/routing';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const intlMiddleware = createMiddleware(routing);

export default function middleware(request: NextRequest) {
  if (request.nextUrl.pathname === '/api/auth/signout') {
    const response = NextResponse.redirect(new URL('/', request.url));
    response.cookies.delete('better-auth.session_token');
    response.cookies.delete('__Secure-better-auth.session_token');
    response.cookies.delete('better-auth.session_data');
    response.cookies.delete('__Secure-better-auth.session_data');
    response.cookies.delete('next-auth.session-token');
    response.cookies.delete('__Secure-next-auth.session-token');
    return response;
  }
  return intlMiddleware(request);
}

export const config = {
  matcher: ['/', '/(en|es|fr|de|it|pt|nl|ru|zh|ja|ko|ar|hi|tr|pl|sv|no|da|fi|el)/:path*', '/api/auth/signout']
};