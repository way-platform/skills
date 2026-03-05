# GCP Integration

## Integration Approaches

| Approach | Mechanism | Credential | Recommended |
|----------|-----------|-----------|-------------|
| **OIDC / Workload Identity Federation** | Spacelift OIDC token exchanged for short-lived GCP token | `GOOGLE_APPLICATION_CREDENTIALS` → credential config JSON | Yes |
| **Native GCP integration** | Spacelift creates SA, injects OAuth token | `GOOGLE_OAUTH_ACCESS_TOKEN` | Legacy |

---

## OIDC / Workload Identity Federation Setup

### Step 1: Create WIF pool + OIDC provider in GCP

1. GCP console → IAM & Admin → **Workload Identity Federation** → **Create Pool**
2. Add OIDC provider to the pool:
   - **Select a provider**: OpenID Connect (OIDC)
   - **Issuer (URL)**: `https://<account>.app.spacelift.io`
   - **Audiences**: `<account>.app.spacelift.io` (hostname only, no scheme)
3. Attribute mappings (SA impersonation mode):
   - `google.subject` → `assertion.sub`
   - `attribute.space` → `assertion.spaceId`
   - Optional: `attribute.caller` → `assertion.callerId` (for direct resource access)
4. Optionally add attribute conditions (CEL) to restrict which tokens can authenticate

> **Warning**: If stack ID exceeds Google's length limit for `google.subject`, use a different custom claim instead.

### Step 2: Grant SA access to WIF pool

1. In WIF pool details, click **Grant access**
2. Select the service account to impersonate
3. Set principals filter: attribute name = `space`, value = full SpaceId from Spacelift
4. Click **Save**

Any token from that Spacelift space can now impersonate the SA.

### Step 3: Download credential config from GCP

After granting access, click **Configure your application**:
- **OIDC ID token path**: `/mnt/workspace/spacelift.oidc`
- **Format type**: `json`
- **Subject token field name**: `access_token`
- Click **Download config**

Edit the downloaded file: remove the `format` field from `credential_source` so it only contains:

```json
"credential_source": {
  "file": "/mnt/workspace/spacelift.oidc"
}
```

### Step 4: Mount config + set env var in Spacelift

Use a Spacelift context (for reuse across stacks) or stack environment directly:
- **Mounted file**: upload `gcp.json` → mounted at e.g. `/mnt/workspace/gcp.json`
- **Env var**: `GOOGLE_APPLICATION_CREDENTIALS` = `/mnt/workspace/gcp.json`

### Step 5: Configure Terraform provider

```hcl
provider "google" {}
# Picks up GOOGLE_APPLICATION_CREDENTIALS automatically
```

---

## Credential Config File (JSON template)

```json
{
  "type": "external_account",
  "audience": "//iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WORKER_POOL_ID}/providers/${IDENTITY_PROVIDER_ID}",
  "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
  "token_url": "https://sts.googleapis.com/v1/token",
  "credential_source": {
    "file": "/mnt/workspace/spacelift.oidc"
  },
  "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/${SERVICE_ACCOUNT_EMAIL}:generateAccessToken",
  "service_account_impersonation": {
    "token_lifetime_seconds": 3600
  }
}
```

Placeholders to substitute:
- `${PROJECT_NUMBER}` — GCP project number (numeric)
- `${WORKER_POOL_ID}` — WIF pool ID
- `${IDENTITY_PROVIDER_ID}` — OIDC provider ID within the pool
- `${SERVICE_ACCOUNT_EMAIL}` — SA email, e.g. `spacelift@my-project.iam.gserviceaccount.com`

---

## Native GCP Integration (Legacy)

Spacelift creates a dedicated SA per stack and injects a short-lived OAuth token.

```hcl
resource "spacelift_gcp_service_account" "this" {
  stack_id = spacelift_stack.this.id

  token_scopes = [
    "https://www.googleapis.com/auth/compute",
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/ndev.clouddns.readwrite",
    "https://www.googleapis.com/auth/devstorage.full_control",
    "https://www.googleapis.com/auth/userinfo.email",
  ]
}
```

Injected env var: `GOOGLE_OAUTH_ACCESS_TOKEN` — automatically picked up by:

```hcl
provider "google" {}
```

Or explicitly:

```hcl
provider "google" {
  access_token = var.GOOGLE_OAUTH_ACCESS_TOKEN
}
```

Grant the SA access in GCP IAM using `spacelift_gcp_service_account.this.service_account_email`.

---

## OIDC Token Structure

- Available as: `SPACELIFT_OIDC_TOKEN` env var and `/mnt/workspace/spacelift.oidc` file
- Valid for 1 hour

### Standard claims

| Claim | Value |
|-------|-------|
| `iss` | `https://<account>.app.spacelift.io` |
| `sub` | `space:<id>:<callerType>:<callerId>:run_type:<type>:scope:<read\|write>` |
| `aud` | `<account>.app.spacelift.io` |
| `exp` | Issued time + 3600s |

### Custom claims

| Claim | Description |
|-------|-------------|
| `spaceId` | Space slug/ID |
| `callerType` | `stack` or `module` |
| `callerId` | Stack or module ID |
| `runType` | `PROPOSED`, `TRACKED`, `TASK`, `TESTING`, `DESTROY` |
| `runId` | Run ULID |
| `scope` | `read` (proposed runs) or `write` (tracked/task/destroy) |

Default `sub` example:
```
space:legacy-01KJMM56VS4W3AL9YZWVCXBX8D:stack:infra:run_type:TRACKED:scope:write
```

---

## Hierarchical Space Access via spacePath

When spaces share slug names (e.g. `/root/production/us-east-1` and `/root/staging/us-east-1`), the default `sub` claim is identical — use the `{spacePath}` custom subject template to disambiguate.

### Setup

1. Organization Settings → Security → **OIDC subject template**, set:
   ```
   space:{spaceId}:space_path:{spacePath}:{callerType}:{callerId}:run_type:{runType}:scope:{scope}
   ```
2. In WIF provider attribute mappings, add:
   - `attribute.spacePath` → `assertion.spacePath`
3. Use CEL attribute condition to scope access:
   ```cel
   attribute.spacePath.startsWith('/root/production/')
   ```

This lets you add sub-spaces under `production` without updating the WIF config.

> **Warning**: Changing the subject template breaks existing trust policies. Update cloud provider trust policies to accept both formats before changing the template.

---

## Direct Resource Access (No Service Account)

Alternative to SA impersonation — grant permissions directly to the WIF identity.

Attribute mappings (different from SA impersonation):
- `attribute.space` → `assertion.spaceId`
- `google.subject` → `assertion.sub`
- `attribute.caller` → `assertion.callerId`

Grant resource-level permissions (e.g. GCS bucket) using the principal:
```
principalSet://iam.googleapis.com/projects/<PROJECT_ID>/locations/global/workloadIdentityPools/<POOL_NAME>/attribute.caller/<STACK_ID>
```

Credential config for direct access omits `service_account_impersonation_url`:

```json
{
  "type": "external_account",
  "audience": "//iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WORKER_POOL_ID}/providers/${IDENTITY_PROVIDER_ID}",
  "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
  "token_url": "https://sts.googleapis.com/v1/token",
  "credential_source": {
    "file": "/mnt/workspace/spacelift.oidc"
  }
}
```

---

## Troubleshooting

### `iam.serviceAccounts.getAccessToken PERMISSION_DENIED`

Cause: stack not authorized to impersonate the SA.

Check:
1. `service_account_impersonation_url` in credential config points to the correct SA email:
   ```
   https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/spacelift@my-project.iam.gserviceaccount.com:generateAccessToken
   ```
2. WIF pool binding conditions match the stack's `spaceId` — only stacks in the listed space can impersonate
