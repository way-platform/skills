---
name: way-typescript-react-style
description: Guide for writing idiomatic, high-quality TypeScript and React code, and for writing or reviewing vitest tests. Use this skill when writing, refactoring, or reviewing TypeScript/React code or test files to ensure adherence to established conventions, React rules, performance best practices, and vitest testing patterns. Trigger proactively when writing React components, TypeScript types, Next.js pages, or vitest tests, or when auditing existing tests.
---

# Way TypeScript & React Style

## Way Specific Conventions

- Define reusable data/logic helpers as top-level pure functions (outside React components); keep component bodies focused on rendering and wiring
- Complex predicates for array methods must be separate named functions
- **Prefer declarative over imperative** — derive values during render rather than storing them in `let`/`useState`; use `map`/`filter`/`reduce` expressions rather than loops that push into an array; use object/array spread to produce new values rather than mutating existing ones
- **Always use early returns** — `if (isLoading) return <Spinner />;` at the top, not `let content` with if/else branches
- **Never use IIFEs** — extract a named function instead: a top-level pure function for derived values, or a named inner function for JSX that closes over component state
- Avoid `as` casts; prefer narrowing, generics, or splitting code paths. Use `as` only when interoperating with external/untyped APIs and add a short justification comment
- Handle undefined args explicitly (no `?? 0` for mandatory params)
- **Do NOT use `useMemo` or `useCallback`** — React Compiler handles memoization. (Project AGENTS.md may define narrow exceptions.)
- **STOP before writing `useEffect`** — most uses are wrong. Evaluate the decision tree in this skill first. Effects are only for synchronizing with external systems.
- **Data fetching hierarchy**: Always use `@connectrpc/connect-query` hooks with generated `*_connectquery.ts` files. Only fall back to raw `@tanstack/react-query` when no generated file exists or the pattern cannot be expressed via connect-query.
- **Hydration**: Never render server-side content that depends on client state (timestamps, `window` checks)

---

## STOP — Before Writing `useEffect`

Effects are an **escape hatch** for synchronizing with external systems — if no external system is involved, you almost certainly don't need one.

### Decision tree

```
About to write useEffect?
│
├─ Responding to a user action (click, submit, drag)?
│  └─ Use an EVENT HANDLER — you know exactly what happened
│
├─ Deriving a value from props or state?
│  └─ COMPUTE DURING RENDER — const fullName = first + ' ' + last
│
├─ Need to reset state when a prop changes?
│  └─ Use the KEY PROP — <Profile key={userId} />
│
├─ Filtering/transforming data?
│  └─ COMPUTE DURING RENDER (useMemo if expensive)
│
├─ Notifying a parent of a state change?
│  └─ Call the callback IN THE SAME EVENT HANDLER
│
├─ Chaining multiple state updates?
│  └─ Calculate ALL next state IN THE EVENT HANDLER
│
└─ Synchronizing with a non-React system (DOM API, WebSocket, browser API)?
   └─ This is the ONE case where useEffect is correct
      └─ Always include cleanup. For subscriptions, prefer useSyncExternalStore.
```

### The top anti-patterns

| Anti-pattern | What to do instead |
|---|---|
| `useState` + `useEffect` to derive a value | Compute during render: `const x = a + b` |
| `useEffect` to filter/transform data | Compute during render (or `useMemo`) |
| `useEffect` to reset state on prop change | `key` prop on the component |
| `useEffect` to respond to a click/submit | Put the logic in the event handler |
| `useEffect` calling parent's `onChange` | Call `onChange` in the event handler |
| Chain of Effects triggering each other | Compute all state changes in one event handler |
| `useEffect` fetching without cleanup | Add `let ignore = false` cleanup (or use `useQuery`) |
| App init in `useEffect([], ...)` | Module-level `let didInit = false` guard |

For detailed examples with incorrect/correct code, see:
- **[useEffect Anti-Patterns](references/useeffect-anti-patterns.md)** — 9 common mistakes with fixes
- **[Better Alternatives](references/useeffect-alternatives.md)** — `useMemo`, `key` prop, lifting state, `useSyncExternalStore`, event handlers

---

## STOP — Before Writing Data Fetching Hooks

**The most common mistake is reaching for raw `@tanstack/react-query` hooks when generated `@connectrpc/connect-query` hooks should be used instead.** This causes redundant boilerplate, breaks transport injection, and bypasses the project's auth/error-handling layer.

### The hierarchy (follow in order)

```
Fetching data from a ConnectRPC service?
│
├─ Is there a generated *_connectquery.ts file for this method?
│  └─ YES → Use @connectrpc/connect-query hooks ← DEFAULT
│     import { useQuery, useMutation } from "@connectrpc/connect-query"
│     import { listThings } from "@/gen/proto/.../*_connectquery"
│     const { data } = useQuery(listThings, { orgPath }, { transport })
│
└─ NO generated file, or need a pattern connect-query can't express?
   └─ Fall back to @tanstack/react-query directly
      import { useQuery } from "@tanstack/react-query"
      (custom queryFn, useInfiniteQuery with complex pagination, etc.)
```

### connect-query patterns

```ts
// READ — useQuery
import { useQuery } from "@connectrpc/connect-query";
import { listThings } from "@/gen/proto/.../things_service-ThingsService_connectquery";
const transport = useClientConfig();
const { data, isLoading } = useQuery(listThings, { orgPath }, { transport });

// Conditional skip — use skipToken (NOT enabled: false)
import { skipToken } from "@tanstack/react-query";
const { data } = useQuery(listThings, orgPath ? { orgPath } : skipToken, { transport });

// WRITE — useMutation
import { useMutation } from "@connectrpc/connect-query";
const { mutate, isPending } = useMutation(deleteThing, {
  transport,
  onError: (error) => toastApiError(error, t("deleteFailed")),
});

// Cache invalidation after mutation
import { createConnectQueryKey } from "@connectrpc/connect-query";
const queryClient = useQueryClient();
queryClient.invalidateQueries({
  queryKey: createConnectQueryKey({ schema: listThings, transport, cardinality: "finite" }),
});

```

### When raw tanstack-query IS appropriate

- Non-RPC fetches (REST endpoints, third-party APIs)
- Complex multi-RPC `queryFn` that composes several calls imperatively
- `useSuspenseQuery` / `useSuspenseInfiniteQuery` if not yet supported by connect-query
- When you need `queryOptions()` helper for SSR prefetching patterns

For the full tanstack-query API reference see [references/tanstack-query.md](references/tanstack-query.md).

---

## TypeScript Style

### Types

- **Never use boxed types** (`Number`, `String`, `Boolean`, `Symbol`, `Object`). Use the lowercase primitives (`number`, `string`, `boolean`, `symbol`, `object`).
- **Never use `any`** unless migrating from JavaScript. Use `unknown` for truly unknown values.
- **Never have unused type parameters** in generics.

### Callbacks

- **Return `void`**, not `any`, for callbacks whose return value is ignored. `void` prevents accidental use of the return value.
- **Don't make callback parameters optional** — callers can always pass a function that accepts fewer arguments.
- **Don't overload on callback arity** — write a single overload with the maximum arity.

### Type Safety in Practice

- **Narrow, don't cast** — use type guards, discriminated unions, and `satisfies` instead of `as`.
- **Prefer `unknown` over `any`** — force explicit narrowing at the call site.
- **Use `satisfies`** to validate a value matches a type without widening it: `const config = { ... } satisfies Config`.
- **Prefer `readonly`** for data that shouldn't be mutated (function parameters, returned arrays).
- **Avoid enums** in application code — use `as const` objects or string literal unions. (Generated proto enums are the exception.)

## React Rules

These are rules, not guidelines — breaking them causes bugs. Condensed from the [official Rules of React](references/react-rules.md).

### 1. Components & Hooks Must Be Pure

- **Idempotent**: Same inputs (props, state, context) must produce the same output. Don't use `new Date()` or `Math.random()` during render — move them to effects or event handlers.
- **No side effects in render**: React can render components multiple times. Side effects belong in event handlers or `useEffect`.
- **Local mutation is fine**: Creating and modifying local variables during render is OK — the mutation isn't remembered between renders.
- **Props, state, and hook return values are immutable**: Never mutate them directly. Use setter functions.
- **Don't mutate values after passing to JSX**: React may evaluate JSX eagerly; mutating after the fact leads to stale UI.

### 2. React Controls Invocation

- **Never call component functions directly** — use them in JSX. React needs to orchestrate rendering, reconciliation, and state management.
- **Never pass hooks around as values** — always call hooks inline. Don't dynamically mutate or inject hooks.

### 3. Rules of Hooks

- **Top level only** — no hooks in loops, conditions, nested functions, try/catch, or after early returns.
- **React functions only** — call hooks from function components or custom hooks, never from regular functions.

## React & Next.js Performance

See `references/vercel-rules/` for the full 57-rule reference. Key patterns:

### Eliminating Waterfalls

- Move `await` into the branch that uses it — don't block early returns with unneeded fetches
- `Promise.all()` for independent operations; start promises early, await late
- Wrap slow data components in `<Suspense>` so the surrounding layout renders immediately
- Sibling async Server Components fetch in parallel; a parent that `await`s before rendering children creates a waterfall

### Bundle Size

- Import directly from source files, not barrel `index.ts` re-exports
- `next/dynamic` for heavy components (maps, editors, charts)
- Defer analytics/logging with `dynamic(() => ..., { ssr: false })`
- Trigger `import()` on hover/focus to preload before click

### Server-Side Performance

- Verify auth inside every Server Action — don't rely on middleware alone
- Pass only the fields a client component actually uses (no 50-field objects)
- Sibling async Server Components fetch in parallel; awaiting in a parent creates a waterfall
- `React.cache()` deduplicates calls within one request (avoid inline object args)
- `after()` for logging/analytics so it doesn't block the response

### Re-render Optimization

- Derive values during render — don't store computed state or sync via effects
- `setState(prev => ...)` when new state depends on previous value
- `useState(() => expensiveInit())` — function form, not expression
- Depend on `user.id` not `user`; derive booleans and depend on those
- `useRef` for transient values (mouse position, timers, flags)
- `startTransition` for non-urgent updates

### Rendering Performance

- **Explicit conditional rendering**: Use ternary (`condition ? <A /> : null`), not `&&`, when the condition could be `0` or `NaN`.
- **Animate SVG wrappers**: Wrap SVG in a `<div>` and animate the wrapper for GPU acceleration.
- **`content-visibility: auto`**: Defer off-screen rendering for long lists.
- **Hydration mismatches**: Use `suppressHydrationWarning` only for expected differences (timestamps, locales). For client-only data (theme), use an inline `<script>` to set the DOM before hydration.

### JavaScript Performance

- `Set`/`Map` for repeated lookups instead of array scans
- `toSorted()` / `toReversed()` / `toSpliced()` — `.sort()` mutates
- Combine multiple `.filter()`/`.map()` passes into one loop
- Hoist `RegExp` to module scope; cache `localStorage` reads in a module-level `Map`

### Advanced Patterns

- **Initialize once per app load**: Don't put one-time init in `useEffect([], ...)` — it re-runs on remount and runs twice in dev. Use a module-level `let didInit = false` guard.
- **`useEffectEvent`**: Creates a stable function reference that always calls the latest handler, without adding the handler to effect dependencies.

## Testing Best Practise

**STOP before writing or reviewing vitest tests** — load [references/testing-best-practices.md](references/testing-best-practices.md) first. It covers the NEVER-do list (untestable files, mock cleanup, loose assertions, testing implementation details, skipping `tsc --noEmit` on test files, and more), the questions to ask before writing a test, the pre-write and test-review workflows, and links to 12 detailed pattern files in `references/testing/` plus the review report template in `assets/testing-output-report-template.md`.

## Available References

Detailed documentation available in the `references/` directory:

- **[useEffect Anti-Patterns](references/useeffect-anti-patterns.md)**: 9 common mistakes with incorrect/correct code examples.
- **[useEffect Alternatives](references/useeffect-alternatives.md)**: `useMemo`, `key` prop, lifting state, `useSyncExternalStore`, event handlers, custom hooks.
- **[TypeScript Do's and Don'ts](references/typescript-dos-and-donts.md)**: Official TypeScript handbook guidance on types, callbacks, and overloads.
- **[Rules of React](references/react-rules.md)**: All four pages of React's official rules — purity, invocation, hooks.
- **[Vercel React Rules](references/vercel-rules/)**: 57 individual rule files with incorrect/correct code examples. Named by category prefix: `async-*`, `bundle-*`, `server-*`, `client-*`, `rerender-*`, `rendering-*`, `js-*`, `advanced-*`. Load individual files on demand rather than the full set.
- **[TanStack Query Reference](references/tanstack-query.md)**: Full API reference for `@tanstack/react-query` v5 — for fallback cases where connect-query is insufficient.
- **[Testing Best Practices](references/testing-best-practices.md)**: Full vitest testing guide — NEVER-do list, pre-write checklist, workflows for writing and reviewing tests, and a table of detailed pattern files.
- **[Vitest Pattern Files](references/testing/)**: 12 files covering organization, AAA pattern, parameterized tests, error handling, assertions, test doubles, async testing, performance, vitest features, snapshot testing, property-based testing, and a quick-start example. Load individual files on demand, per the table in [testing-best-practices.md](references/testing-best-practices.md).
- **[Test Review Report Template](assets/testing-output-report-template.md)**: Standardized format for test code review/audit findings — severity levels, impact analysis, and a summary table.
