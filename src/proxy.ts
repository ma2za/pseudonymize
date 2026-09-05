import createMiddleware from 'next-intl/middleware';
import {routing} from './i18n/routing';

export default createMiddleware(routing);

export const config = {
  matcher: ['/', '/(en|es|fr|de|it|pt|nl|ru|zh|ja|ko|ar|hi|tr|pl|sv|no|da|fi|el)/:path*']
};