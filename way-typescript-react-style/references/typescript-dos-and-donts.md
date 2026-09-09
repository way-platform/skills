# TypeScript Do's and Don'ts

Source: https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html

## General Types

### Number, String, Boolean, Symbol and Object

**Don't** ever use the types `Number`, `String`, `Boolean`, `Symbol`, or `Object`. These types refer to non-primitive boxed objects that are almost never used appropriately in JavaScript code.

```ts
/* WRONG */
function reverse(s: String): String;
```

**Do** use the types `number`, `string`, `boolean`, and `symbol`.

```ts
/* OK */
function reverse(s: string): string;
```

Instead of `Object`, use the non-primitive `object` type.

### Generics

**Don't** ever have a generic type which doesn't use its type parameter.

### any

**Don't** use `any` as a type unless you are in the process of migrating a JavaScript project to TypeScript. The compiler effectively treats `any` as "please turn off type checking for this thing". In cases where you don't know what type you want to accept, or when you want to accept anything because you will be blindly passing it through without interacting with it, you can use `unknown`.

### as any / as unknown

**Don't** cast with `as any`, or with `as unknown` (including the `as unknown as T` double-cast idiom). Both are enforced by lint (`no-explicit-any` for `as any`; the `as unknown` text scan in `pnpm validate:syntax`) and will fail `pnpm check`.

**Do** narrow with a type guard, or fix the type at its source (the schema, the proto, the third-party type declaration) instead of casting around it. If a value is genuinely untyped at a boundary (e.g. `JSON.parse`, a third-party callback), declare it `unknown` and narrow with a guard — do not cast it straight to the target type.

```ts
/* WRONG */
const config = rawConfig as unknown as ChartConfig;

/* OK */
function isChartConfig(value: unknown): value is ChartConfig {
  return typeof value === "object" && value !== null && "series" in value;
}
if (!isChartConfig(rawConfig)) {
  throw new Error("Invalid chart config");
}
const config = rawConfig;
```

## Metabase TypeScript/JavaScript Development Skill

Source: https://www.skills.sh/metabase/metabase/typescript-write. Metabase-specific
tools/paths adapted to Way's equivalents (`pnpm typecheck` instead of `bun run
type-check-pure`, proto/generated types instead of `metabase-types/api`,
`typescript/switch-exhaustiveness-check` instead of `ts-pattern`).

### No `any` — hard rule

- **New code must not introduce `any`, explicit or implicit.** No `any` annotations, no `as any` / `as unknown as`, no untyped parameters or returns that infer `any`, no implicitly-`any` destructures or array/object literals.
- **Untyped third-party / boundary values** must be typed at the boundary (a declared type, `unknown` + type guard, or a small typed wrapper) — never let `any` propagate inward.
- **Mandatory type verification.** Before finishing a TS/TSX change, run `pnpm typecheck`.

### Type tightening

- **Avoid type casts and loose `unknown`** — fix the signature instead.
- **If a function only needs one field of a wide object, accept that field** — not the wide object. The cast often disappears once the signature is right.
- **Reach for `Partial<T>`, `Pick<T, K>`, `Record<K, V>`, and generics** before reaching for a cast.
- **Prefer making props/components generic** (`<T>`) when a value flows through unchanged and the caller knows the type.
- **Prefer `unknown` over loose typing** and narrow before use — an `unknown` value forces a guard at the point of use.
- **`satisfies` for object literals** that must conform without widening (config objects, lookup maps, discriminated literals) — better than `: T` (widens) or `as T` (unsafe).
- **Avoid non-null assertions (`!`)**. Prefer a guard, early return, or `?.`. Use `!` only when non-nullness is provably true and localized, with a comment.
- **No redundant runtime coercion** — don't wrap already-typed values in `Number()` / `String()` / `Boolean()`.
- **Type guards belong next to the type they narrow** — do not redefine the same guard in multiple files.
- **A cast you can't avoid needs a real justification comment.** State the actual reason the cast is safe. If you can't articulate why the cast is correct, the cast is wrong — fix the types.

### Type modeling

- **Reuse existing types; don't re-declare them.** Use the generated proto/`FooJson` types and Way's own domain types (`ViewId`, path types, etc.) and key data structures by them. Don't duplicate generated/API types — compose or derive (`Pick`, `Omit`, indexed access `SomeType["field"]`, `ReturnType`).
- **Use generics to allow TypeScript to infer correct types** when creating functions and components that need to be reusable and type-safe. Don't hesitate to introduce complex generics if they allow deriving types automatically instead of manual narrowing.
- **Model the actual data contract; keep types narrow.** Optional `field?: T` for a key that may be absent, `field: T | undefined` only when the key is always present but the value may be undefined, `| null` for explicit API nulls. Prefer domain unions over broad `string` / `number` / loose `Record`.
- **Refer to the proto/API implementation** when defining or refining types to ensure they match the actual data structure. When considering a type cast, first consider if the type should be refined to match the actual data structure.
- **Discriminated unions for variant state, with exhaustive checks.** Model "one of N shapes" as a union with a literal discriminant rather than a bag of optional fields, and exhaust it in a `switch` — `typescript/switch-exhaustiveness-check` (enabled repo-wide) makes adding a variant without handling it a compile-time lint error.
- **Derive union types from constants** (`as const` + `typeof`/`keyof`) so the type and the values can't drift.
- **`readonly` / immutability where mutation isn't intended** — component props, shared constants, exported config. Prefer `readonly T[]` / `ReadonlyArray<T>` for inputs you don't mutate.
- **Type async and error states explicitly** (a discriminated union or the data-layer's typed result) — never leave loading/error/empty implicit.

### Null and undefined

- **Narrow at the source**. If a value is optional only in a corner case, don't thread `undefined` through every layer — guard at the producer.
- **Sensible defaults for optional values**. Use `?.` and `??` at the consumer.
- **Lists should be filtered** before being used in a map or other iteration.
- **Avoid non-strict null comparisons** (`X != null`) when `X` can never be `null` — use a strict check or narrow the type instead.
- **Check actual nullability against the proto/API implementation**. Confirm whether a field can actually be absent or null before assuming it.

Naming, code structure, and comments guidance from this skill live in
`SKILL.md`'s "Way Specific Conventions" section, not duplicated here.

### Verify before done

- **Run `pnpm check`** when finished.

## Callback Types

### Return Types of Callbacks

**Don't** use the return type `any` for callbacks whose value will be ignored -- use `void` instead. Using `void` is safer because it prevents you from accidentally using the return value in an unchecked way.

### Optional Parameters in Callbacks

**Don't** use optional parameters in callbacks unless you really mean it. It's always legal to provide a callback that accepts fewer arguments, so there's no need to make callback parameters optional.

### Overloads and Callbacks

**Don't** write separate overloads that differ only on callback arity. Write a single overload using the maximum arity. It's always legal for a callback to disregard a parameter.

## Function Overloads

### Ordering

**Do** sort overloads by putting the more general signatures after more specific signatures. TypeScript chooses the first matching overload when resolving function calls.

### Use Optional Parameters

**Do** use optional parameters instead of writing several overloads that differ only in trailing parameters (when all overloads have the same return type).

### Use Union Types

**Do** use union types instead of writing overloads that differ by type in only one argument position. This is important for people who are "passing through" a value to your function.
