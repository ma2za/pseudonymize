import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/db"; 
import * as schema from "@/db/schema";
import { Resend } from 'resend';

const resend = process.env.RESEND_API_KEY ? new Resend(process.env.RESEND_API_KEY) : null;

export const auth = betterAuth({
    database: drizzleAdapter(db, {
        provider: "pg", 
        schema: {
            user: schema.user,
            session: schema.session,
            account: schema.account,
            verification: schema.verification
        }
    }),
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
});