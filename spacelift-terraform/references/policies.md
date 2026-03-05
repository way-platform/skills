# Spacelift Policies

## Table of Contents
- [Policy Types Overview](#policy-types-overview)
- [Rego v1 Basics](#rego-v1-basics)
- [Policy Attachment](#policy-attachment)
- [Push Policy](#push-policy)
- [Plan Policy](#plan-policy)
- [Trigger Policy](#trigger-policy)
- [Approval Policy](#approval-policy)
- [Other Policy Types](#other-policy-types)
- [Policy Workbench](#policy-workbench)

---

## Policy Types Overview

| Type | Fires when | Key outputs |
|------|-----------|-------------|
| **Push** | Git push or PR event received | `track`, `propose`, `ignore`, `notify`, `cancel` |
| **Plan** | After `terraform plan` succeeds | `deny`, `warn` |
| **Trigger** | Tracked run or task reaches terminal state | `trigger` (stack IDs) |
| **Approval** | Run enters queued/unconfirmed/pending-review | `approve`, `reject` |
| **Login** | User attempts to log in | `allow`, `deny`, `admin` |
| **Stack Access** | User accesses a stack | `read`, `write`, `admin`, `deny` |
| **Notification** | Any run state change | `slack`, `webhook` (notification targets) |
| **Task** | Before a task runs | `allow`, `deny` |
| **Run Initialization** | Before run starts on worker | `allow`, `deny` (deprecated — use worker-side) |

For our GitHub+Terraform use case, focus on: **Push**, **Plan**, **Trigger**, **Approval**.

---

## Rego v1 Basics

All policies use OPA Rego v1 syntax (`package spacelift`).

```opa
package spacelift

# Set-based rules (preferred in Rego v1)
deny contains "message" if { condition }
warn contains "message" if { condition }

# Boolean rules
approve if { condition }
track if { condition }

# Iteration
some item in collection
```

### Rego v1 vs v0 Differences

```opa
# Rego v1 (use this)
deny contains "msg" if { true }
cancel contains run.id if { some run in input.in_progress }

# Rego v0 (legacy)
deny["msg"] { true }
cancel[run.id] { run := input.in_progress[_] }
```

---

## Policy Attachment

### Manual Attachment

Attach via stack Settings → Policies tab. Select policy and click Attach.

### Auto-Attach via Labels

Add label to policy: `autoattach:label-name`

Any stack with matching label `label-name` automatically gets the policy attached.

Useful for org-wide baseline policies (e.g., all stacks get a cost-limit plan policy).

### Evaluation Timeout

Default: 5 seconds. Policies that exceed this timeout are treated as if they returned no rules.

---

## Push Policy

Fires on each push or PR event, per stack.

### Outputs

| Rule | Effect |
|------|--------|
| `track` | Create tracked run (can apply) |
| `propose` | Create proposed run (plan only) |
| `ignore` | No run |
| `notify` | Send notification (no run) |
| `cancel` contains run IDs | Cancel those in-progress runs |

Default (no policy): push to tracked branch → track; push to other branch → propose if PR exists.

### Key Input Fields

```json
{
  "push": {
    "branch": "string",
    "affected_files": ["path/to/file.tf"],
    "tag": "string or null",
    "message": "string",
    "creator_login": "string"
  },
  "pull_request": {
    "action": "opened | synchronized | closed | labeled | review_requested",
    "draft": false,
    "labels": ["string"],
    "head": { "branch": "string", "sha": "string" },
    "base": { "branch": "string" },
    "id": 12345,
    "mergeable": true
  },
  "stack": {
    "id": "string",
    "branch": "string",
    "project_root": "string or null",
    "labels": ["string"]
  },
  "in_progress": [
    { "id": "string", "type": "PROPOSED | TRACKED", "state": "QUEUED | READY" }
  ]
}
```

### Examples

**Standard GitOps:**
```opa
package spacelift

track if input.push.branch == input.stack.branch
propose if not is_null(input.pull_request)
ignore if { not track; not propose }
```

**Path-filtered (monorepo):**
```opa
package spacelift

relevant_change if {
  some file in input.push.affected_files
  startswith(file, concat("", [input.stack.project_root, "/"]))
}

track if {
  input.push.branch == input.stack.branch
  relevant_change
}

propose if {
  not is_null(input.pull_request)
  relevant_change
}

ignore if { not track; not propose }
```

**Cancel stale proposed runs on new push:**
```opa
package spacelift

cancel contains run.id if {
  some run in input.in_progress
  run.type == "PROPOSED"
  run.state == "QUEUED"
}
```

---

## Plan Policy

Fires after `terraform plan` succeeds. Has full access to planned resource changes.

### Outputs

| Rule | Effect |
|------|--------|
| `deny` contains message | Fail run (shown in red) |
| `warn` contains message | Mark for human review if autodeploy; shown in yellow |

`warn` with autodeploy: run pauses at **unconfirmed** state, requiring manual confirmation.

### Key Input Fields

```json
{
  "spacelift": {
    "run": {
      "type": "TRACKED | PROPOSED",
      "branch": "string",
      "triggered_by": "string or null",
      "drift_detection": false,
      "changes": [
        {
          "action": "added | changed | deleted",
          "entity": {
            "address": "aws_s3_bucket.example",
            "name": "example",
            "type": "aws_s3_bucket",
            "entity_vendor": "aws",
            "entity_type": "resource",
            "data": {}
          },
          "phase": "plan | apply"
        }
      ]
    },
    "stack": {
      "id": "string",
      "branch": "string",
      "labels": ["string"]
    }
  },
  "terraform": {
    "resource_changes": [ /* full terraform plan JSON */ ]
  }
}
```

### Examples

**Block IAM resource creation:**
```opa
package spacelift

deny contains sprintf("IAM resource %s not allowed", [change.entity.address]) if {
  some change in input.spacelift.run.changes
  change.action == "added"
  startswith(change.entity.type, "aws_iam_")
}
```

**Warn on deletions (require review):**
```opa
package spacelift

warn contains sprintf("Deleting %s requires review", [change.entity.address]) if {
  some change in input.spacelift.run.changes
  change.action == "deleted"
}
```

**Require manual review for drift reconciliation:**
```opa
package spacelift

warn contains "Drift reconciliation requires manual approval" if {
  input.spacelift.run.drift_detection
}
```

**Block deploy from GitHub PR (not from merge):**
```opa
package spacelift

deny contains "Deploy only via merge, not directly from GitHub" if {
  input.spacelift.run.type == "TRACKED"
  startswith(input.spacelift.run.triggered_by, "github/")
}
```

---

## Trigger Policy

Fires when a tracked run or task reaches a terminal state. Used to cascade runs across stacks.

**Prefer stack dependencies** for simple chains; use trigger policies for complex conditional logic.

### Terminal States

`FINISHED`, `CANCELED`, `DISCARDED`, `STOPPED`, `FAILED`

### Output

`trigger` contains stack IDs to trigger a tracked run on.

### Key Input Fields

```json
{
  "run": {
    "id": "string",
    "type": "TRACKED | TASK",
    "state": "FINISHED | FAILED | ...",
    "branch": "string",
    "drift_detection": false,
    "changes": [ /* resource changes */ ]
  },
  "stack": { "id": "string", "name": "string", "labels": ["string"] },
  "stacks": [ /* all stacks in account with same schema */ ],
  "workflow": [ /* all runs in current workflow */ ]
}
```

### Examples

**Trigger dependents on success:**
```opa
package spacelift

trigger contains stack.id if {
  input.run.state == "FINISHED"
  some stack in input.stacks
  some label in stack.labels
  label == concat("", ["depends-on:", input.stack.id])
}
```

**Retry on failure (max 1 retry):**
```opa
package spacelift

trigger contains input.stack.id if {
  input.run.state == "FAILED"
  count([r | some r in input.workflow; r.state == "FAILED"]) < 2
}
```

---

## Approval Policy

Fires when run enters **queued**, **unconfirmed**, or **pending-review** state.

### Outputs

| Rule | Effect |
|------|--------|
| `approve` | Run proceeds |
| `reject` | Run fails immediately |
| Neither | `undecided` — more reviews needed |

`approve` not defined → run stays blocked until explicitly approved or rejected in UI.

Users need **write** or **admin** stack access to submit reviews.

### Key Input Fields

```json
{
  "reviews": {
    "current": {
      "approvals": [
        {
          "author": "username",
          "session": { "login": "string", "teams": ["string"] },
          "state": "queued | unconfirmed"
        }
      ],
      "rejections": [ /* same schema */ ]
    },
    "older": [ /* reviews for previous states */ ]
  },
  "run": {
    "type": "TRACKED",
    "state": "unconfirmed",
    "triggered_by": "string",
    "branch": "string",
    "changes": [ /* resource changes */ ]
  },
  "stack": { "id": "string", "labels": ["string"] }
}
```

### Examples

**Require 1 approval from any reviewer:**
```opa
package spacelift

approve if count(input.reviews.current.approvals) >= 1
reject if count(input.reviews.current.rejections) >= 1
```

**Require approval from specific team:**
```opa
package spacelift

approved_by_team if {
  some approval in input.reviews.current.approvals
  some team in approval.session.teams
  team == "infra-leads"
}

approve if approved_by_team
```

**Two-person rule (approver can't be the triggerer):**
```opa
package spacelift

valid_approval if {
  some approval in input.reviews.current.approvals
  approval.session.login != input.run.triggered_by
}

approve if valid_approval
```

---

## Other Policy Types

### Login Policy

Controls who can authenticate to Spacelift.

```opa
package spacelift

# Allow org members, deny everyone else
allow if input.session.teams[_] == "my-github-org"
deny if not allow
admin if input.session.teams[_] == "platform-team"
```

### Stack Access Policy

Fine-grained stack-level RBAC.

```opa
package spacelift

# Writers: infra team
write if input.session.teams[_] == "infra-team"

# Readers: everyone in org
read if input.session.teams[_] == "my-github-org"
```

---

## Policy Workbench

Test policies against sample inputs before attaching to stacks.

- Navigate to: Policies → select policy → Workbench tab
- Paste custom JSON input matching the schema
- View policy evaluation results in real time
- Sample inputs available from existing run evaluations (Policies → Samples)
