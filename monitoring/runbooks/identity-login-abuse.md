# LoginLockoutSpike / LoginThrottleSpike / IdentityDown

**Meaning.** `stackshop_auth_logins_total{outcome="locked_out"|"throttled"}` is rising sharply: credential stuffing, brute force, or a misbehaving client. `IdentityDown` means no identity target is scraped.

**Check.**
1. Dashboard "Identity & Auth": compare success, invalid_credentials, locked_out and throttled.
2. High `throttled` with normal traffic: the gateway may not be forwarding `X-Forwarded-For`, so all users share one IP bucket. Identity trusts that header, so only the gateway may reach it (NetworkPolicy `identity`).
3. Check the gateway `auth-strict` limiter (5 req/min per IP) and its logs for the source addresses.
4. IdentityDown: `kubectl -n stackshop get pods -l app.kubernetes.io/name=identity`; check the `identity-secrets` Secret (signing key mounted at /keys/private.pem), MySQL and Redis reachability, and the last migration Job.

**Fix.** Block abusive sources at the ingress/WAF, change `Auth__LockoutMinutes` or `Auth__IpAttemptLimit` in the overlay ConfigMap (needs a rollout), or fix the client.
