# Identity service health (5xx and latency)

Alerts: `IdentityHighErrorRate` (critical), `IdentityHighLatencyP95` (warning).
Dashboard: **Identity & Auth**, row "Service health (RED)" and "Runtime resources".

## 1. Confirm and scope
- Open the dashboard. Is it all routes or one? "Request rate by route" and "p95 latency by route" show which endpoint.
- Login is the slowest endpoint by design (password hashing); a high p95 on `/auth/login` alone with normal CPU is often a login burst, check the login abuse runbook.

## 2. Check dependencies
- **MySQL**: `docker logs stackshop-backend-identity-1` (local) or `kubectl -n stackshop logs deploy/identity` for connection errors or timeouts.
- **Redis**: errors from the jti blacklist or login throttle. Note the blacklist fails open if Redis is down (revoked tokens are accepted until they expire, up to 15 minutes).
- **SMTP**: email failures do not fail requests today (the queue is in memory), so they will not show here.

## 3. Check the process
- "Memory" growing without bound: possible leak, restart the pod and capture a heap dump if it repeats.
- "Thread pool" queue length above 0 for minutes: the service is saturated, scale out (HPA max is 5, prod 6) or find the blocking call.
- "Exceptions and GC": a spike in exceptions/s usually matches the 5xx ratio.

## 4. Mitigate
- Roll back the last deploy if the alert started right after one (see the promote-release flow).
- Scale: `kubectl -n stackshop scale deploy/identity --replicas=4` (HPA will take over again).
