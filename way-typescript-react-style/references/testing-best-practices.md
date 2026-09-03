# Vitest Best Practices

Comprehensive patterns for writing maintainable, effective vitest tests. Focused on expert-level guidance for test organization, clarity, and performance.

## NEVER Do When Writing Vitest Tests

- **NEVER write tests for files with no behavior** - Constants files (just `export const X = value`), type definition files, GLSL uniform declarations, and pure data files contain no logic to test. Testing `expect(MY_CONSTANT).toBe(42)` verifies nothing: if the value changes, the test changes with it, providing zero protection. These "tests" waste CI time and create maintenance burden when values change. Test behavior (functions, logic, transformations), not data declarations. If a file exports only types, constants, or data structures with no functions or logic, skip testing it entirely.
- **NEVER skip global mock cleanup configuration** - Manual cleanup appears safe but creates "action at a distance" failures: a mock in test file A leaks into test file B running 3 files later, causing non-deterministic failures that only appear when tests run in specific orders. These Heisenbugs waste hours in CI debugging. Configure `clearMocks: true`, `mockReset: true`, `restoreMocks: true` in `vitest.config.ts` once to eliminate this entire class of order-dependent failure.
- **NEVER nest describe blocks more than 2 levels deep** - Deep nesting creates cognitive overhead and excessive indentation. Put context in test names instead: `it('should add item to empty cart')` vs `describe('when cart is empty', () => describe('addItem', ...))`.
- **NEVER write test descriptions that don't read as sentences** - Test descriptions must complete the sentence "it ..." in lowercase. Write `it('should add item to cart')` not `it('Add item to cart')` or `it('It should add item to cart')`. The description reads as a sentence when prefixed with "it": "it should add item to cart". Capitalized starts, non-sentence formats like `it('addToCart test')`, or redundant "It should" break readability and test output consistency. Example-based tests use `it('should...')` while property-based tests use `it('property: ...')` format.
- **NEVER test library internals that the library already tests** - Testing `expect(array.map(fn)).toEqual(expected)` wastes time verifying that Array.prototype.map works correctly. The JavaScript/TypeScript standard library and established third-party libraries are already well-tested. Focus tests on your business logic, not on proving that lodash, React, or the language itself works. If you find yourself testing "does this library function do what it claims?", you're testing the wrong layer. Test how your code uses libraries, not whether libraries work.
- **NEVER export internal functions just to test them** - Tests should verify behavior through the public API, not reach into implementation details. Exporting private helpers, internal utilities, or implementation functions solely to enable testing is a code smell that indicates either: (1) the public API is insufficient for testing the behavior, or (2) the tests are verifying implementation details instead of behavior. If internal logic is complex enough to warrant dedicated testing, extract it into a separate module with its own public API and test file. Private functions get tested indirectly through the public functions that call them.
- **NEVER mock your own pure functions** - Mocking internal code makes tests brittle and less valuable. Mock only external dependencies (APIs, databases, third-party libraries). Prefer fakes > stubs > spies > mocks.
- **NEVER use loose assertions like `toBeTruthy()` or `toBeDefined()`** - These assertions pass for multiple distinct values you never intended: `toBeTruthy()` passes for `1`, `"false"`, `[]`, and `{}` - all semantically different. When refactoring changes `getUser()` from returning `{id: 1}` to returning `1`, your test still passes but your production code breaks. Loose assertions create false confidence that evaporates in production. `toBeTypeOf()` is NOT a loose assertion.
- **NEVER test implementation details instead of behavior** - Tests that verify "function X was called 3 times" create false failures: you optimize code to call X once via memoization, all tests fail, yet the user experience is identical (and faster). These tests actively punish performance improvements and refactoring. Test what users observe (outputs given inputs), not how your code achieves it internally.
- **NEVER share mutable state between tests** - Tests that depend on execution order or previous test state create flaky, unreliable suites. Each test must be fully independent with fresh setup.
- **NEVER use `any` or skip type checking in test files** - When implementation signatures change, tests with `as any` silently pass while calling functions with wrong arguments. You ship broken code that TypeScript could have caught. Tests are executable documentation: `user as any` communicates nothing, but `createTestUser(Partial<User>)` shows exactly what properties matter for this test case.
- **NEVER mark test files as complete without running TypeScript type checking** - Test files are typically excluded from `tsconfig.json` compilation paths, so running `tsc` at the project root won't catch type errors in tests. Type errors in tests cause runtime failures, incorrect test behavior, and false confidence from tests that don't test what they claim. Before marking any test file as "done", you MUST run `tsc --noEmit` directly against the test file using the project's package manager (npm/pnpm/bun/yarn). For monorepos, `cd` into the specific package directory first, then run type checking. Fix all type errors before proceeding - never use `as any` or `@ts-ignore` to bypass errors.
- **NEVER assume TypeScript types prevent runtime errors** - TS types are compile-time only and vanish at runtime. Testing only "type-valid" inputs creates a false sense of security. In production, functions receive invalid data from JSON APIs without validation, `JSON.parse()` results, external libraries, user input, and database records. A function typed as `process(data: ValidData)` can still receive `null`, `undefined`, or malformed objects at runtime. Test defensive programming scenarios: pass `null` to non-nullable parameters, `undefined` to required fields, malformed objects to typed parameters. These "type-invalid" tests catch real bugs that TypeScript cannot prevent.
- **NEVER write weak properties when stronger ones exist** - Property-based tests that only verify "no exception thrown" or "returns a value" provide minimal coverage. When testing encode/decode pairs, verify roundtrip equality (`decode(encode(x)) === x`), not just that decode succeeds. When testing normalization, verify idempotence (`normalize(normalize(x)) === normalize(x)`), not just that it returns a string. Weak properties give false confidence: they pass but don't actually validate correctness.

## Before Writing Tests, Ask

Apply these expert thinking patterns before implementing tests:

### Should This File Be Tested?
- **Does this file contain behavior to test?** Files that only declare constants, types, or data structures without logic don't need tests. Constants files (`export const X = 42`), type definition files (`type User = {...}`), GLSL uniform declarations, configuration objects, and pure data files have no behavior to verify. If the file contains no functions, no logic, no transformations - skip testing it. Test behavior, not data.

### Test Isolation and Setup
- **Where should cleanup logic live?** Think in layers: configuration eliminates entire error classes (mock cleanup in vitest.config.ts), setup files handle project-wide concerns (custom matchers, global mocks), beforeEach handles test-specific state. Each test doing its own mock cleanup is like each function doing its own null checks - it works but misses the point. Push concerns to the highest appropriate layer.
- **Does this test depend on previous tests or shared state?** Test suites are parallel universes - each test should work identically whether it runs first, last, or alone. State dependency creates "quantum tests" that pass or fail based on execution order. If a test needs data from another test, they're actually one test split artificially.

### What to Test
- **Am I testing behavior or implementation?** Test what users experience (inputs → outputs), not how code achieves it (which functions were called). Implementation tests break during safe refactoring.
- **What's the simplest dependency I can use?** Real implementation > fake > stub > spy > mock. Each step down this hierarchy adds brittleness. Mock only when using real code is impractical (external APIs, slow operations).

### Test Clarity
- **Can someone understand this test in 5 seconds?** Follow AAA pattern (Arrange, Act, Assert) with clear boundaries. If setup is complex, extract to helper functions with descriptive names.
- **Are there multiple variations of the same behavior?** Use `it.each()` for parameterized tests instead of copying test structure. One assertion per concept keeps tests focused.

### Performance and Maintenance
- **Will this test still be valuable in 6 months?** Avoid testing framework internals or trivial operations. Focus on business logic, edge cases, and error handling that actually prevent bugs.
- **Is this test fast enough to run on every save?** Avoid expensive operations in tests. Use fakes for databases, mock timers for delays, stub external calls. Tests should complete in milliseconds.

## Workflow: Before Writing Tests

**0. Verify the file contains testable behavior**
Before writing any tests, check if the file actually needs testing:
- Does it contain functions or logic? → Test it
- Does it only export constants, types, or data? → Skip testing it

Files without behavior (constants files, type definitions, GLSL uniform declarations, pure data files) don't need tests. Testing `expect(CONSTANT).toBe(value)` provides no value and wastes CI time.

**1. Check vitest.config.ts for global configuration**
Verify mock cleanup is configured globally:
```ts
// Look for these settings:
clearMocks: true      // Mock cleanup configured?
mockReset: true       // Mock reset configured?
restoreMocks: true    // Mock restore configured?
```

If not present, recommend adding them. This eliminates the entire class of mock cleanup errors.

**2. Discover existing test setup files**
Check common locations for test setup configuration:
- `test/setup.{ts,js}` or `testing/setup.{ts,js}`
- `vitest.setup.{ts,js}` or `src/test/setup.{ts,js}`
- Check `vitest.config.ts` for configured `setupFiles` and `globalSetup`

**3. Analyze setup file contents**
When found, identify:
- Global mocks (fetch, timers, etc.)
- Custom matchers (e.g., `@testing-library/jest-dom`)
- Test utilities and helpers
- Environment configuration

**4. Only add per-test cleanup for non-mock resources**
If global config handles mocks, DO NOT add manual mock cleanup:
- ❌ Don't add `vi.clearAllMocks()` (handled by config)
- ✅ Do clean up listeners, connections, custom state

**Principle: Configuration over repetition**
Mock cleanup is a safety concern. Configure it once globally to make forgetting impossible. Manual cleanup in every test violates DRY and creates maintenance burden.

See [vitest-features.md](testing/vitest-features.md#discovering-existing-setup-files) and [performance.md](testing/performance.md#cleanup-between-tests) for detailed examples.

## Workflow: Before Marking Test Files Complete

**CRITICAL: This workflow is MANDATORY. Never skip type checking test files.**

Before marking any test file as "complete" or "done", verify type correctness:

**Why this matters:** Test files are typically excluded from `tsconfig.json` compilation (not in `include` paths), so running `tsc` at the project root won't catch type errors in tests. Type errors in tests can cause:
- Runtime failures that should have been caught at compile time
- Incorrect test behavior due to type mismatches
- False confidence from tests that don't actually test what they claim

**Verification steps:**

1. **Navigate to the package directory (CRITICAL for monorepos):**
For monorepos or multi-package projects, you MUST `cd` into the specific package directory before running type checking. TypeScript needs to run from where the `tsconfig.json` and `node_modules` are located for that package.

```bash
# Example for monorepo:
cd packages/my-package
# Then run tsc from here
```

2. **Check test file directly with TypeScript:**
Use the project's package manager to run TypeScript:
```bash
# Detect which package manager to use:
# - npm: npm exec tsc -- --noEmit path/to/test.test.ts
# - pnpm: pnpm exec tsc --noEmit path/to/test.test.ts
# - bun: bunx tsc --noEmit path/to/test.test.ts
# - yarn: yarn exec tsc --noEmit path/to/test.test.ts
```

To detect the package manager, check for:
- `bun.lockb` or `bun.lock` → use `bunx`
- `pnpm-lock.yaml` → use `pnpm exec`
- `yarn.lock` → use `yarn exec`
- `package-lock.json` → use `npm exec`

2. **Look for common type issues:**
- Mock types not matching actual implementation types
- Test data with missing or incorrect properties
- Assertion types that don't match expected values
- Missing type parameters on generic functions
- Incorrect use of type guards or type assertions

3. **Fix all type errors before marking complete (NON-NEGOTIABLE)**
This step is MANDATORY, not optional. Type errors in tests are as critical as type errors in production code.
- Do NOT use `as any` or `@ts-ignore` to bypass type checking
- Update test data to match actual types
- Fix mock return types to match implementation
- Add proper type annotations where TypeScript cannot infer
- If you encounter type errors, STOP and fix them - do not proceed with "I'll fix types later"

**Example type errors to catch:**

```typescript
// ❌ Type error: property 'email' is missing
const user = createUser({ name: 'Alice' })

// ✅ Correct: all required properties provided
const user = createUser({ name: 'Alice', email: 'alice@example.com' })

// ❌ Type error: vi.fn() returns unknown, not User
const mockGetUser = vi.fn().mockReturnValue({ id: 1 })

// ✅ Correct: explicitly type the mock
const mockGetUser = vi.fn<() => User>().mockReturnValue({ id: 1, name: 'Alice', email: 'test@example.com' })
```

**Principle: Type-safe tests prevent silent failures**
Type errors in tests are as critical as type errors in production code. Catch them before marking work complete.

**CRITICAL REMINDER:** This workflow is NOT optional. Running `tsc --noEmit` against test files is a REQUIRED step before marking test work as complete. If you skip this step, you risk shipping broken tests that provide false confidence.

## Workflow: Test Code Review/Audit

When reviewing existing test code (skill invoked with file path or user asks to "review tests" or "audit tests"), follow this systematic approach:

**1. Load property-based-testing.md for pattern detection**
Always load [property-based-testing.md](testing/property-based-testing.md) during test audits to check for PBT opportunities.

**2. Identify anti-patterns and violations**
Check for violations of rules in sections 1.1-1.11 below.

**3. Check for property-based testing opportunities**
For each test file, analyze the code under test and identify high-value PBT patterns:

**ALWAYS check for these patterns:**
- **Encode/decode pairs**: Functions like `encode()`/`decode()`, `serialize()`/`deserialize()`, `toJSON()`/`fromJSON()` → Suggest roundtrip property
- **Normalization functions**: `normalize()`, `sanitize()`, `format()` → Suggest idempotence property
- **Validator + normalizer pairs**: `isValid()` + `normalize()` → Suggest "isValid(normalize(x)) always true"
- **Pure transformation functions**: No side effects, deterministic → Multiple properties may apply
- **Sorting/ordering functions**: `sort()`, `compare()` → Suggest ordering + idempotence properties
- **Data structure operations**: Custom collections with invariants → Suggest invariant properties

**When identifying PBT opportunities:**
- Check if fast-check is installed (`package.json` devDependencies)
- If installed: Recommend PBT improvements directly
- If NOT installed: Suggest PBT as an option with user approval required

**4. Generate report using template**
Use [../assets/testing-output-report-template.md](../assets/testing-output-report-template.md) and include PBT opportunities in a dedicated section.

**Example PBT opportunity detection:**

```typescript
// Code under test:
function get<T>(obj: Record<string, T>, path: string): T | undefined

// Example-based test found:
it('gets nested value', () => {
  expect(get({ a: { b: 1 } }, 'a.b')).toBe(1)
})

// PBT opportunity identified:
// ✅ EXCELLENT CANDIDATE for property-based testing
// Pattern: Pure function with clear invariants
// Properties to test:
// 1. get(obj, path) returns undefined for non-existent paths
// 2. get(obj, path) preserves type (type preservation)
// 3. get(obj, path) never throws on valid inputs
```

**Principle: Proactive improvement suggestions**
Don't wait for users to ask "would any benefit from PBT?" — proactively identify and suggest PBT opportunities as part of every test audit.

---

## 1. General

### 1.1 Organization
Place test files next to implementation; one test file per module.
[View detailed examples](testing/organization.md)

### 1.2 AAA Pattern
Structure tests as Arrange, Act, Assert for clarity.
[View detailed examples](testing/aaa-pattern.md)

### 1.3 Parameterized Tests
Use `it.each` for variations; one behavior per test.
[View detailed examples](testing/parameterized-tests.md)

### 1.4 Error Handling
Test negative cases, fault injection, and recovery thoroughly.
[View detailed examples](testing/error-handling.md)

### 1.5 Assertions
Use strict assertions (`toEqual`, `toStrictEqual`) over loose ones.
[View detailed examples](testing/assertions.md)

### 1.6 Test Doubles
Prefer fakes > stubs > spies/mocks; avoid over-mocking.
[View detailed examples](testing/test-doubles.md)

### 1.7 Async Testing
Test promises, async/await, and timers correctly.
[View detailed examples](testing/async-testing.md)

### 1.8 Performance
Keep tests fast through efficient setup and avoiding expensive operations.
[View detailed examples](testing/performance.md)

### 1.9 Vitest Features
Use coverage, watch mode, benchmarking, and other vitest-specific features.
[View detailed examples](testing/vitest-features.md)

### 1.10 Snapshot Testing
Use snapshots for appropriate cases; avoid common pitfalls.
[View detailed examples](testing/snapshot-testing.md)

### 1.11 Property-Based Testing
Use fast-check for stronger coverage with generated inputs; test encode/decode pairs, validators, normalizers, and invariants.
[View detailed examples](testing/property-based-testing.md)

## Quick Example

See [testing/quick-start.md](testing/quick-start.md) for a complete before/after example showing how this guide transforms unclear tests into clear, maintainable ones.
