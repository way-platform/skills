# Worker Pools

## Table of Contents
- [Public vs Private Workers](#public-vs-private-workers)
- [Setup: Create a Private Worker Pool](#setup-create-a-private-worker-pool)
- [Launching Workers](#launching-workers)
- [Configuration Variables](#configuration-variables)
- [Network Requirements](#network-requirements)
- [Worker Status and Management](#worker-status-and-management)
- [Hardware Sizing](#hardware-sizing)
- [Drift Detection Run Limits](#drift-detection-run-limits)

---

## Public vs Private Workers

| | Public Workers | Private Workers |
|--|----------------|----------------|
| Hosted by | Spacelift | You |
| IAM/credentials | Trust relationship with Spacelift AWS | Assumes your cloud role directly |
| Docker registries | Public only | Public + private |
| Drift detection | Not supported | Supported |
| Autoretry | Not supported | Supported |
| Network access | From Spacelift's infra | From your infra |
| Maintenance | Spacelift-managed | You manage updates |
| Custom runner images | Public only | Public + private registry |

**Use private workers when:**
- Drift detection required
- Access to private registries or internal services
- Compliance requires runs in your environment
- Custom runner images from private registries

---

## Setup: Create a Private Worker Pool

### Step 1: Generate Private Key and CSR

```bash
openssl req -new -newkey rsa:4096 -nodes \
  -keyout spacelift.key \
  -out spacelift.csr
```

**Store `spacelift.key` securely** — this is your pool's private key. You'll need it when launching workers.

### Step 2: Create Pool in Spacelift

1. _Manage Organization_ → _Worker Pools_ → **Create worker pool**
2. Enter:
   - **Name**: descriptive, unique
   - **Certificate**: upload `spacelift.csr`
   - **Space**: which space owns this pool
   - **Labels**: for filtering/policy use
3. Click **Create**

You receive a **Spacelift worker pool token** (base64-encoded). Store securely — needed for worker launch.

### Step 3: Launch Workers

See [Launching Workers](#launching-workers).

---

## Launching Workers

### Docker-Based

```bash
docker run \
  -e SPACELIFT_TOKEN=<worker-pool-token> \
  -e SPACELIFT_PRIVATE_KEY="$(cat spacelift.key)" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  public.ecr.aws/spacelift/launcher:latest
```

### Kubernetes

Use the Spacelift Worker Pool Controller:
```bash
helm repo add spacelift https://downloads.spacelift.io/helm
helm install spacelift-worker-pool-controller spacelift/spacelift-worker-pool-controller
```

Create a `WorkerPool` CR referencing the token and key as secrets.

### Terraform (via Spacelift Provider)

```hcl
resource "spacelift_worker_pool" "main" {
  name        = "production-workers"
  description = "Production Terraform runners"
  space_id    = "root"
  csr         = filebase64("spacelift.csr")
}
```

---

## Configuration Variables

### Shared Options (Docker + Kubernetes)

| Variable | Description |
|----------|-------------|
| `SPACELIFT_TOKEN` | Worker pool token (from pool creation) |
| `SPACELIFT_PRIVATE_KEY` | Private key content (from `spacelift.key`) |
| `SPACELIFT_MASK_ENVS` | Comma-delimited env vars to mask in logs |
| `SPACELIFT_SENSITIVE_OUTPUT_UPLOAD_ENABLED` | `true` to enable sensitive stack outputs (for stack dependencies) |
| `SPACELIFT_RUN_LOGS_ON_STANDARD_OUTPUT_ENABLED` | `true` to write structured run logs to stdout |
| `SPACELIFT_LAUNCHER_LOGS_TIMEOUT` | Timeout for runs producing no logs (default: 7 min). Format: `1000s` |
| `SPACELIFT_LAUNCHER_RUN_TIMEOUT` | Max run duration (default: 70 min). Format: `120m` |
| `SPACELIFT_DEBUG` | `true` to log exact commands run |

### Docker-Only Options

| Variable | Description |
|----------|-------------|
| `SPACELIFT_WHITELIST_ENVS` | Env vars to pass from launcher to worker containers. Prefix `ro_` (read-only runs) or `wo_` (write-only runs) |
| `SPACELIFT_DOCKER_CONFIG_DIR` | Docker config dir (for private registry auth) |
| `SPACELIFT_WORKER_EXTRA_MOUNTS` | Extra mounts for all runs: `/host/path:/container/path,...` |
| `SPACELIFT_WORKER_RO_EXTRA_MOUNTS` | Extra mounts for read-only (proposed) runs |
| `SPACELIFT_WORKER_WO_EXTRA_MOUNTS` | Extra mounts for write-only (tracked) runs |
| `SPACELIFT_WORKER_NETWORK` | Docker network (default: `bridge`) |
| `SPACELIFT_DEFAULT_RUNNER_IMAGE` | Override default runner image for all stacks on this pool |

### Metadata Tags

Pass `SPACELIFT_METADATA_*` vars to tag workers for identification:

```bash
export SPACELIFT_METADATA_instance_id=$(ec2-metadata --instance-id | cut -d ' ' -f2)
export SPACELIFT_METADATA_region=us-east-1
```

---

## Network Requirements

Workers initiate all connections (no inbound required):

| Endpoint | Protocol | Purpose |
|----------|---------|---------|
| `*.app.spacelift.io` | HTTPS (443) | Spacelift API |
| `*.app.spacelift.io` | MQTT (8883) | Run scheduling messages |
| `*.s3.amazonaws.com` | HTTPS (443) | Run state and artifact storage |
| `public.ecr.aws` | HTTPS (443) | Default runner images |
| GitHub / VCS | HTTPS (443) | Source code checkout |

Workers poll Spacelift via MQTT for run assignments — no inbound ports needed.

---

## Worker Status and Management

### Worker States

| State | Meaning |
|-------|---------|
| `IDLE` | Ready to accept runs |
| `BUSY` | Processing a run |
| `DRAINED` | No longer accepting new runs (graceful shutdown) |

### Draining a Worker

```bash
# Via spacectl
spacectl workerpool drain-worker --id <pool-id> --worker <worker-id>
```

Use drain before terminating a worker to avoid orphaned runs.

### Scaling

- Each worker handles **one run at a time**
- Scale out = more workers = more parallelism
- Typical setup: one worker per EC2/VM instance

---

## Hardware Sizing

Sizing depends on Terraform project size and provider complexity.

### Minimum Recommendations

| Workload | CPU | Memory |
|----------|-----|--------|
| Small stacks (<100 resources) | 1 vCPU | 2 GB |
| Medium stacks (100-500 resources) | 2 vCPU | 4 GB |
| Large stacks (500+ resources) | 4 vCPU | 8 GB |

### Storage

- Minimum 20 GB for Docker images and run workspaces
- More if using large provider plugin caches

### Terraform Plugin Cache (Performance)

Mount a shared plugin cache to avoid re-downloading providers:

```bash
SPACELIFT_WORKER_EXTRA_MOUNTS=/host/tf-plugin-cache:/root/.terraform.d/plugin-cache
```

Set `TF_PLUGIN_CACHE_DIR=/root/.terraform.d/plugin-cache` via context.

---

## Drift Detection Run Limits

Configure at worker pool level to prevent resource exhaustion from drift runs.

- **No limit** (default): drift runs have no concurrency cap
- **Numeric limit**: max N concurrent drift detection runs on this pool
- **Disabled**: no drift detection on this pool (creates failed run records for tracking)

Configure: _Manage Organization_ → _Worker Pools_ → pool → Edit → **Configure drift detection run limits**

Use cases:
- Cap drift runs so regular tracked runs aren't starved
- Disable during maintenance windows
- Cost control on expensive worker types
