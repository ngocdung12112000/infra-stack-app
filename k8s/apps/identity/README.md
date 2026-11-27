# identity: Kubernetes manifests

Image `ghcr.io/ngocdung12112000/stackshop-identity`, port 8080, ClusterIP Service on 80. Reachable only from
the gateway (X-Forwarded-For is trusted) and Prometheus (`/metrics`), see `base/networkpolicy.yaml`.

## Secret `identity-secrets` (never committed in plain text)

| Key | Used for |
|-----|----------|
| `ConnectionStrings__Identity` | MySQL connection string (schema `identity`, user `identity`) |
| `Redis__ConnectionString` | Redis (login throttling, refresh state) |
| `Email__Username`, `Email__Password` | SMTP credentials (optional) |
| `signing-private-key.pem` | RS256 private key, mounted at `/keys/private.pem` (`Signing__PrivateKeyPath`) |
| `Signing__KeyId`, `Signing__RetiredPublicKeyPems__0` | optional, for key rotation (old public key stays in the JWKS) |

- dev: create out of band (or seal it), e.g.
  `openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out key.pem` then
  `kubectl -n stackshop create secret generic identity-secrets --from-literal=ConnectionStrings__Identity=... --from-literal=Redis__ConnectionString=... --from-file=signing-private-key.pem=key.pem` (run by a human against the cluster).
- staging: SealedSecret (`overlays/staging/sealedsecret.yaml` is an empty placeholder).
- prod: ExternalSecret (`overlays/prod/externalsecret.yaml`) reading AWS Secrets Manager `stackshop/prod/identity`.

`Signing__GenerateIfMissing` is `false` here; the pods fail fast without a key.

## Gateway env (apply when `k8s/apps/gateway` exists)

```
Jwt__JwksUrl=http://identity:8080/.well-known/jwks.json
Redis__ConnectionString=<redis in data ns>
ReverseProxy__Clusters__identity__Destinations__primary__Address=http://identity:8080/
# The Service exposes both 80 and 8080 (both -> container port 8080).
```
