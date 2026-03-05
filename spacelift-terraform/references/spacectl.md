# spacectl CLI Reference

## Table of Contents
- [Installation](#installation)
- [Authentication](#authentication)
- [Stack Operations](#stack-operations)
- [Run Management](#run-management)
- [Worker Pool Commands](#worker-pool-commands)
- [Agent Workflow Patterns](#agent-workflow-patterns)
- [GraphQL API Access](#graphql-api-access)

---

## Installation

```bash
# Homebrew (macOS/Linux)
brew install spacelift-io/spacelift/spacectl

# asdf
asdf plugin add spacectl
asdf install spacectl latest
asdf global spacectl latest

# Docker
docker run -it --rm ghcr.io/spacelift-io/spacectl <command>

# GitHub Actions
- uses: spacelift-io/setup-spacectl@main
```

Download binaries from: https://github.com/spacelift-io/spacectl/releases

---

## Authentication

### Method 1: Environment Variables (CI/agent use)

```bash
export SPACELIFT_API_KEY_ENDPOINT=https://myorg.app.spacelift.io
export SPACELIFT_API_KEY_ID=<key-id>
export SPACELIFT_API_KEY_SECRET=<key-secret>
```

Or with a short-lived token:
```bash
export SPACELIFT_API_TOKEN=<token>
```

Precedence: `SPACELIFT_API_TOKEN` > `SPACELIFT_API_GITHUB_TOKEN` > API key vars

### Method 2: Profile (interactive/local use)

```bash
# Create profile (browser auth)
spacectl profile login myorg
# Enter endpoint: https://myorg.app.spacelift.io
# Select option 3 (browser)

# Create profile (API key auth)
spacectl profile login myorg
# Select option 1 (API key)

# List profiles
spacectl profile list

# Switch profiles
spacectl profile select myorg

# Show current
spacectl profile current

# Export token for scripting
spacectl profile export-token
```

### Method 3: GitHub Actions Full Example

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: spacelift-io/setup-spacectl@main

      - name: Deploy
        env:
          SPACELIFT_API_KEY_ENDPOINT: https://myorg.app.spacelift.io
          SPACELIFT_API_KEY_ID: ${{ secrets.SPACELIFT_API_KEY_ID }}
          SPACELIFT_API_KEY_SECRET: ${{ secrets.SPACELIFT_API_KEY_SECRET }}
        run: spacectl stack deploy --id my-stack --auto-confirm
```

---

## Stack Operations

```bash
# List all stacks
spacectl stack list

# Show stack details
spacectl stack show --id <stack-id>

# Deploy (trigger tracked run)
spacectl stack deploy --id <stack-id>

# Deploy and auto-confirm (skip unconfirmed state)
spacectl stack deploy --id <stack-id> --auto-confirm

# Deploy and wait for completion
spacectl stack deploy --id <stack-id> --auto-confirm --tail

# Preview (trigger proposed run)
spacectl stack preview --id <stack-id>

# Local preview (upload current directory)
spacectl stack local-preview --id <stack-id>

# Run a one-off task
spacectl stack task --id <stack-id> --tail 'terraform output -json'

# Set environment variable
spacectl var set --id <stack-id> --name MY_VAR --value myvalue

# Set secret variable
spacectl var set --id <stack-id> --name MY_SECRET --value myvalue --secret
```

---

## Run Management

```bash
# List runs for a stack
spacectl run list --stack <stack-id>

# Show run details
spacectl run show --stack <stack-id> --run <run-id>

# Stream run logs
spacectl run logs --stack <stack-id> --run <run-id>

# Confirm a run (unconfirmed → applying)
spacectl run confirm --stack <stack-id> --run <run-id>

# Discard a run
spacectl run discard --stack <stack-id> --run <run-id>

# Stop a run
spacectl run stop --stack <stack-id> --run <run-id>
```

---

## Worker Pool Commands

```bash
# List worker pools
spacectl workerpool list

# Show worker pool details
spacectl workerpool show --id <pool-id>

# List workers in a pool
spacectl workerpool workers --id <pool-id>

# Drain a worker (stop accepting new runs)
spacectl workerpool drain-worker --id <pool-id> --worker <worker-id>
```

---

## Agent Workflow Patterns

### Non-Interactive CI Authentication

Never use browser auth in CI. Use API keys:

```bash
# Set these as CI secrets, then export in pipeline
export SPACELIFT_API_KEY_ENDPOINT=https://myorg.app.spacelift.io
export SPACELIFT_API_KEY_ID=$CI_SPACELIFT_KEY_ID
export SPACELIFT_API_KEY_SECRET=$CI_SPACELIFT_KEY_SECRET
```

### Wait for Stack to Finish

```bash
# Deploy and tail logs until complete
spacectl stack deploy --id networking-stack --auto-confirm --tail
echo "Exit: $?"
```

### Trigger + Poll Pattern (custom wait)

```bash
# Trigger
spacectl stack deploy --id my-stack

# Get latest run ID
RUN_ID=$(spacectl run list --stack my-stack --output json | jq -r '.[0].id')

# Stream logs
spacectl run logs --stack my-stack --run $RUN_ID
```

### Multi-Stack Orchestration

```bash
# Sequential deployment
spacectl stack deploy --id base-networking --auto-confirm --tail
spacectl stack deploy --id platform --auto-confirm --tail
spacectl stack deploy --id applications --auto-confirm --tail
```

### Local Preview in CI

```bash
# Upload local workspace as proposed run (useful for pre-PR validation)
spacectl stack local-preview --id my-stack --tail
```

### Export Token for Subprocesses

```bash
# Get a short-lived bearer token
TOKEN=$(spacectl profile export-token)
curl -H "Authorization: Bearer $TOKEN" \
  https://myorg.app.spacelift.io/graphql \
  -d '{"query": "{ stacks { id name } }"}'
```

---

## GraphQL API Access

For operations not available in the CLI, use the GraphQL API directly.

### Endpoint

```
https://<account>.app.spacelift.io/graphql
```

### Auth Header

```
Authorization: Bearer <token>
```

Get token via: `spacectl profile export-token`

### Common Queries

```graphql
# List stacks
query {
  stacks {
    id
    name
    state
    branch
  }
}

# Get stack by ID
query {
  stack(id: "my-stack") {
    id
    name
    state
    trackedCommit { hash branch author }
  }
}

# Trigger tracked run
mutation {
  runResourceCreate(
    stack: "my-stack"
    proposedRun: false
  ) {
    id
    state
  }
}
```

### Schema Introspection

```bash
# Fetch policy contract schema
curl https://myorg.app.spacelift.io/.well-known/policy-contract.json | jq '.PLAN'
```

Use this to get exact input shapes for each policy type.
