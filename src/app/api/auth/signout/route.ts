import { NextResponse } from 'next/server';
import { auth } from '@/lib/auth';

export async function GET(request: Request) {
    try {
        await auth.api.signOut({
            headers: request.headers,
        });
    } catch (e) {
        console.error("Signout error", e);
    }
    
    const url = new URL(request.url);
    const origin = url.origin;
    const response = NextResponse.redirect(`${origin}/`);
    
    // Explicitly delete cookies
    response.cookies.set('better-auth.session_token', '', { maxAge: 0, path: '/' });
    response.cookies.set('__Secure-better-auth.session_token', '', { maxAge: 0, path: '/' });
    response.cookies.set('better-auth.session_data', '', { maxAge: 0, path: '/' });
    response.cookies.set('__Secure-better-auth.session_data', '', { maxAge: 0, path: '/' });
    response.cookies.set('better-auth.dont_remember', '', { maxAge: 0, path: '/' });
    response.cookies.set('__Secure-better-auth.dont_remember', '', { maxAge: 0, path: '/' });
    
    return response;
}

export async function POST(request: Request) {
    return GET(request);
}
