# RefreshTokenReuseDetected

**Meaning.** A refresh token that was already rotated was presented again (`stackshop_auth_refresh_total{outcome="reused"}`). Identity treats this as theft and revokes the token family, so the legitimate user is logged out too.

**Check.**
1. Dashboard "Identity & Auth" (uid `stackshop-identity-auth`): is `reused` rising alone, or together with `invalid`?
2. Identity logs (no PII): `kubectl -n stackshop logs deploy/identity | grep -i reuse`.
3. Rule out a client bug. A frontend that calls `/auth/refresh` in parallel (two tabs, stale cookie after a deploy) produces benign reuse. `proxy.ts` should serialise refresh (ADR-003).

**Fix.** Benign: fix the client race. Real theft: confirm affected families are revoked, force a password reset for those users, and rotate the signing key if the key may be exposed (set `Signing__KeyId`, keep the old public key in `Signing__RetiredPublicKeyPems__0`).
