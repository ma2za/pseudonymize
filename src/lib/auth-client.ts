import { createAuthClient } from "better-auth/react"

// Ensure we don't fall back to localhost in production if the env var is missed during Docker build.
// If we are in the browser, we just use the current origin.
const getBaseURL = () => {
    if (typeof window !== 'undefined') {
        return window.location.origin;
    }
    return process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000";
};

export const authClient = createAuthClient({
    baseURL: getBaseURL(),
})