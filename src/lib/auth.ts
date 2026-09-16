import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { nextCookies } from "better-auth/next-js";
import { prisma } from "@/db"; 
import { Resend } from 'resend';

const resend = process.env.RESEND_API_KEY ? new Resend(process.env.RESEND_API_KEY) : null;

export const auth = betterAuth({
    secret: process.env.BETTER_AUTH_SECRET,
    baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
    database: prismaAdapter(prisma, {
        provider: "postgresql",
    }),
    rateLimit: { enabled: false },
    databaseHooks: {
        user: {
            create: {
                after: async (user) => {
                    if (!resend) return;
                    try {
                        await resend.emails.send({
                            from: 'pseudonymize.io <noreply@pseudonymize.io>',
                            to: 'mazzapaolo2019@gmail.com',
                            subject: 'New User Registration: ' + user.email,
                            html: `<p>A new user registered on pseudonymize.io:</p><ul><li>Name: ${user.name}</li><li>Email: ${user.email}</li></ul>`
                        });
                    } catch (e) {
                        console.error('Failed to send admin notification email:', e);
                    }
                }
            }
        }
    },
    trustedOrigins: [
        "https://pseudonymize.io", 
        "https://www.pseudonymize.io", 
        "http://localhost:3000"
    ],
    emailAndPassword: {
        enabled: true,
        sendResetPassword: async (data, request) => {
            if (!resend) return;
            try {
                await resend.emails.send({
                    from: 'pseudonymize.io <noreply@pseudonymize.io>',
                    to: data.user.email,
                    subject: 'Reset your password',
                    html: `<p>Click <a href="${data.url}">here</a> to reset your password.</p>`
                });
            } catch (e) {
                console.error('Failed to send reset password email:', e);
            }
        }
    },
    emailVerification: {
        sendOnSignUp: true,
        sendVerificationEmail: async (data, request) => {
            if (!resend) return;
            try {
                await resend.emails.send({
                    from: 'pseudonymize.io <noreply@pseudonymize.io>',
                    to: data.user.email,
                    subject: 'Verify your email address',
                    html: `<p>Click <a href="${data.url}">here</a> to verify your email address.</p>`
                });
            } catch (e) {
                console.error('Failed to send verification email:', e);
            }
        }
    },
    socialProviders: {
        google: {
            clientId: process.env.GOOGLE_CLIENT_ID as string,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
        }
    },
    plugins: [nextCookies()],
});