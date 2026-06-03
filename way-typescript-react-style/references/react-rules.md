# Rules of React

Source: https://react.dev/reference/rules (and all subpages)

These are **rules** -- not guidelines. Breaking them means your app likely has bugs.

---

## 1. Components and Hooks Must Be Pure

Pure functions only perform a calculation and nothing more. Purity makes code easier to understand, debug, and allows React to automatically optimize components and Hooks.

### Components must be idempotent

Components must always return the same output with respect to their inputs (props, state, context). All code that runs during render must also be idempotent.

- `new Date()` is not idempotent -- don't use it during render
- `Math.random()` is not idempotent -- don't use it during render
- Move non-idempotent code into Effects or event handlers

### Side effects must run outside of render

Side effects should not run in render, as React can render components multiple times. Use event handlers for user-triggered side effects. Use `useEffect` only as a last resort for synchronizing with external systems.

**When is mutation okay?**

- **Local mutation**: Creating and modifying local variables during render is fine. The key point is that the mutation isn't "remembered" between renders.
- **Lazy initialization**: Also fine despite not being fully "pure".
- **Changing the DOM**: Side effects directly visible to the user are not allowed in render logic. Synchronize with `useEffect`.

### Props and state are immutable

Props and state are immutable snapshots. Never mutate them directly. Pass new props down, and use the setter function from `useState`.

- Don't mutate props -- the application will produce inconsistent output
- Don't mutate state variables -- use the setter function to inform React of changes

### Return values and arguments to Hooks are immutable

Once values are passed to a Hook, don't modify them. Like props in JSX, values become immutable when passed to a Hook. A custom hook might have used its arguments as dependencies to memoize values inside it.

### Values are immutable after being passed to JSX

Don't mutate values after they've been used in JSX. Move the mutation to before the JSX is created. React may eagerly evaluate JSX before the component finishes rendering.

---

## 2. React Calls Components and Hooks

React is responsible for rendering components and Hooks when necessary to optimize the user experience. It is declarative: you tell React what to render, and React figures out how best to display it.

### Never call component functions directly

Components should only be used in JSX. Don't call them as regular functions. React must decide when your component function is called during rendering.

**Why React must orchestrate rendering:**

- Components become more than functions -- React augments them with features like local state through Hooks
- Component types participate in reconciliation
- React can enhance user experience (e.g., letting the browser do work between component calls)
- Better debugging story
- More efficient reconciliation -- React can skip re-rendering unchanged components

### Never pass around Hooks as regular values

Hooks should only be called inside of components or Hooks. Never pass them around as a regular value. This enables local reasoning -- the ability for developers to understand everything a component can do by looking at it in isolation.

- **Don't dynamically mutate a Hook** -- Hooks should be immutable. Don't write higher-order Hooks that mutate them.
- **Don't dynamically use Hooks** -- Don't do dependency injection by passing a Hook as a value. Always inline the call.

---

## 3. Rules of Hooks

### Only call Hooks at the top level

**Don't call Hooks inside loops, conditions, nested functions, or `try`/`catch`/`finally` blocks.** Always use Hooks at the top level of your React function, before any early returns.

You can only call Hooks while React is rendering a function component:

- Call them at the top level in the body of a function component
- Call them at the top level in the body of a custom Hook

**Not supported:**

- Inside conditions or loops
- After a conditional `return` statement
- In event handlers
- In class components
- Inside functions passed to `useMemo`, `useReducer`, or `useEffect`
- Inside `try`/`catch`/`finally` blocks

### Only call Hooks from React functions

Don't call Hooks from regular JavaScript functions. Call Hooks from:

- React function components
- Custom Hooks

By following this rule, all stateful logic in a component is clearly visible from its source code.
