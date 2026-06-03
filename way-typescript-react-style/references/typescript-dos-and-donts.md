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
