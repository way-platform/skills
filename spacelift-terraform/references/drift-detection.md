# Drift Detection

## Table of Contents
- [How Drift Detection Works](#how-drift-detection-works)
- [Prerequisites](#prerequisites)
- [Configuring Drift Detection Schedule](#configuring-drift-detection-schedule)
- [Reconciliation](#reconciliation)
- [Viewing Drifted Resources](#viewing-drifted-resources)
- [Plan Policy Integration](#plan-policy-integration)
- [Trigger Policy Integration](#trigger-policy-integration)
- [Drift Detection Run Limits](#drift-detection-run-limits)

---

## How Drift Detection Works

Drift = difference between desired state (Terraform config) and actual state (cloud resources).

**Sources of drift:**
1. Manual changes by humans/scripts outside Terraform
2. Resources depending on dynamic external data sources

**Detection mechanism:**
- Spacelift periodically runs **proposed runs** on stacks in `FINISHED` state
- If plan shows no changes → no drift
- If plan shows changes → drift detected
- Drifted resources appear in Resources view

Drift detection runs are identical to manually triggered proposed runs, with one difference: `input.spacelift.run.drift_detection = true` in policy input.

---

## Prerequisites

- **Private worker pool required** — drift detection does not work on public workers
- Stack must be in `FINISHED` state (not locked, failed, etc.)

---

## Configuring Drift Detection Schedule

### Via UI

1. Stack → **Scheduling** tab → **Drift Detection** section
2. Click **Create drift detection schedule**
3. Add one or more cron expressions
4. Toggle **Reconciliation** (optional)

### Via Terraform Provider

```hcl
resource "spacelift_drift_detection" "every_6h" {
  stack_id      = spacelift_stack.production.id
  reconcile     = true
  ignore_state  = false
  schedule      = ["0 */6 * * *"]  # every 6 hours
  timezone      = "UTC"
}
```

### Cron Examples

| Schedule | Cron |
|----------|------|
| Every 6 hours | `0 */6 * * *` |
| Daily at midnight | `0 0 * * *` |
| Every 30 minutes | `*/30 * * * *` |
| Weekdays at 9am | `0 9 * * 1-5` |

---

## Reconciliation

When reconciliation is enabled, Spacelift triggers a **tracked run** when drift is detected.

- Reconciliation run follows same rules as manual tracked runs:
  - `autodeploy: true` → auto-apply
  - `autodeploy: false` → pauses at **unconfirmed** state
  - Plan policy `warn` → pauses at **unconfirmed** (even with autodeploy)
  - Approval policies evaluated normally

**Require manual approval for drift reconciliation (plan policy):**
```opa
package spacelift

warn contains "Drift reconciliation requires manual approval" if {
  input.spacelift.run.drift_detection
}
```

This causes reconciliation runs to always pause at unconfirmed, even with autodeploy enabled.

### Reconciliation Without Auto-Apply

Set `reconcile: true` with `autodeploy: false` on the stack:
- Drift detected → tracked run created
- Run pauses at unconfirmed
- Human reviews and confirms

---

## Viewing Drifted Resources

### Stack Level

Stack → **Resources** tab → filter by drifted status

Resources with unreconciled drift show drift indicator.

### Account Level

_Account_ → _Resources_ → filter by `driftDetection: true`

Shows all drifted resources across all stacks.

### In Run History

_Account_ → _Runs_ → filter by **Drift Detection** parameter

Shows all drift detection run history with outcomes.

---

## Plan Policy Integration

The `drift_detection` flag is available in plan policy input:

```json
{
  "spacelift": {
    "run": {
      "drift_detection": true,
      ...
    }
  }
}
```

### Pattern: Different rules for drift vs regular runs

```opa
package spacelift

# Block all deletions in normal runs, warn in drift runs
deny contains sprintf("Deletion of %s not allowed", [change.entity.address]) if {
  some change in input.spacelift.run.changes
  change.action == "deleted"
  not input.spacelift.run.drift_detection
}

warn contains sprintf("Drift: %s would be deleted", [change.entity.address]) if {
  some change in input.spacelift.run.changes
  change.action == "deleted"
  input.spacelift.run.drift_detection
}
```

---

## Trigger Policy Integration

Trigger policy also receives `drift_detection` flag on the run:

```opa
package spacelift

# Don't cascade drift detection runs to dependent stacks
trigger contains dep_stack.id if {
  input.run.state == "FINISHED"
  not input.run.drift_detection
  some dep_stack in input.stacks
  some label in dep_stack.labels
  label == concat("", ["depends-on:", input.stack.id])
}
```

### Notify on Drift Detection

Use trigger policy to notify when drift is found:

```opa
package spacelift

# Trigger a notification stack when drift is detected with changes
trigger contains "drift-notifier-stack" if {
  input.run.drift_detection
  input.run.state == "FINISHED"
  count(input.run.changes) > 0
}
```

---

## Drift Detection Run Limits

Configured at the **worker pool** level (not stack level).

**Options:**
- No limit (default)
- Numeric cap (max N concurrent drift runs on pool)
- Disabled (no drift runs on this pool)

**Behavior when disabled:**
- Drift detection runs are prevented
- Failed run records are created with explanatory notes (for audit trail)

**Use cases:**
- Prevent drift runs from starving regular tracked runs
- Temporarily disable during maintenance
- Cost control on expensive worker pools

Configure: _Manage Organization_ → _Worker Pools_ → pool → Edit

See `references/worker-pools.md` for details.
