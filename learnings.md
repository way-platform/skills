# ACT Conformance Testing — Learnings

Learnings from running the PACT/iLEAP ACT conformance suite against
a Go implementation and fixing failures.

---

## TC20: OData `$filter` with Timezone Offset Breaks URL Parsing

**Symptom:** `PACT TC20: Get Filtered List of Footprints — FAILED`
with `Expected status [200], but got 400`.

**Root cause:** ACT sends timestamps with `+00:00` timezone offsets
(not `Z`) in OData filter values, e.g.:

```
GET /2/footprints?$filter=updated+lt+'2023-06-27T13:00:00.000+00:00'
```

Go's `url.ParseQuery` (used by `r.URL.Query()`) decodes `+` as a
space in query strings. The `+` separator between filter tokens
(`updated+lt+`) decodes correctly to spaces, but the `+` inside
the timestamp (`T13:00:00.000+00:00`) also decodes to a space:

```
updated lt '2023-06-27T13:00:00.000 00:00'
```

If the filter parser then splits by whitespace with `strings.Fields`,
it sees 4 tokens instead of 3 → parse error → 400.

**Fix:** Use `strings.SplitN(data, " ", 3)` instead of
`strings.Fields(data)` when parsing a filter predicate. Splitting
into at most 3 parts keeps the RHS intact regardless of spaces it
contains.

```go
// Before — breaks on +HH:MM timezone in RHS
fields := strings.Fields(data)
if len(fields) != 3 { ... }

// After — RHS captures everything after the operator
fields := strings.SplitN(data, " ", 3)
if len(fields) != 3 { ... }
```

**Verification approach:** Send the exact filter to the deployed
server with both `Z` and `+00:00` forms to confirm the `+` decoding
is the culprit:

```sh
# Works: Z suffix
curl ".../2/footprints?\$filter=updated+lt+'2023-06-27T13:00:00.000Z'"

# Fails before fix: +00:00 decoded as space
curl ".../2/footprints?\$filter=updated+lt+'2023-06-27T13:00:00.000+00:00'"
```

---

## TC21: CloudEvents `specversion` Must Be Validated as `"1.0"`

**Symptom:** `PACT TC21: Failed to Receive Notification of PCF Update
— Malformed Request — FAILED` with `Expected status [400], but got 200`.

**Root cause:** ACT sends a CloudEvent with `specversion: "0.3"` (an
older, pre-1.0 CloudEvents version) for the malformed-request test
case, expecting the server to reject it. Checking only for an empty
specversion (`specversion == ""`) passes the wrong version through.

**Fix:** Validate the exact required value:

```go
// Before — accepts any non-empty specversion
if event.Specversion == "" || event.ID == "" || event.Source == "" {

// After — enforces CloudEvents v1.0
if event.Specversion != "1.0" || event.ID == "" || event.Source == "" {
```

**Why this matters:** The PACT spec builds on CloudEvents v1.0.
A server MUST reject events that don't declare the correct specversion,
since the semantics of fields differ between CloudEvents versions.

---

## Debugging Methodology for Unexpected ACT Failures

When ACT returns an unexpected status code, probe the deployed server
directly with `curl` to isolate the cause before reading code:

1. **Obtain a token** from the auth endpoint directly.
2. **Reproduce the exact request** the Rust reference test sends (see
   `references/demo-api/src/main.rs` for test URLs).
3. **Vary one dimension at a time** — e.g., change the timestamp
   suffix from `Z` to `+00:00`, or the specversion from `"1.0"` to
   `"0.3"` — to identify the exact trigger.
4. **Extract strings from the ACT binary** (`strings conformance_x86_64`)
   to surface error messages and field names that hint at what the
   test checks.

This approach avoids guessing at the ACT internals and quickly
confirms or rules out hypotheses.

---

## Known Permanent ACT Failures (Not Implementation Bugs)

| TC | Reason |
|---|---|
| PACT TC8 | Requires short-lived / expired tokens; not practical to provision |
| PACT TC18 | OIDC discovery flow; fails on the SINE reference API too |
| PACT TC19 | Structurally depends on TC18 |
