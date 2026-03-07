---
source_url: https://beam.apache.org/documentation/transforms/python/elementwise/pardo/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "ParDo"
beam_last_updated: "Last updated on 2026/03/06"
---

# ParDo

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.ParDo) |

A transform for generic parallel processing.
A `ParDo` transform considers each element in the input `PCollection`,
performs some processing function (your user code) on that element,
and emits zero or more elements to an output `PCollection`.

See more information in the
[Beam Programming Guide](/documentation/programming-guide/#pardo).

## Examples

In the following examples, we explore how to create custom `DoFn`s and access
the timestamp and windowing information.

### Example 1: ParDo with a simple DoFn

The following example defines a simple `DoFn` class called `SplitWords`
which stores the `delimiter` as an object field.
The `process` method is called once per element,
and it can yield zero or more output elements.

### Example 2: ParDo with timestamp and window information

In this example, we add new parameters to the `process` method to bind parameter values at runtime.

- [`beam.DoFn.TimestampParam`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.DoFn.TimestampParam)
  binds the timestamp information as an
  [`apache_beam.utils.timestamp.Timestamp`](https://beam.apache.org/releases/pydoc/current/apache_beam.utils.timestamp.html#apache_beam.utils.timestamp.Timestamp)
  object.
- [`beam.DoFn.WindowParam`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.DoFn.WindowParam)
  binds the window information as the appropriate
  [`apache_beam.transforms.window.*Window`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.window.html)
  object.

### Example 3: ParDo with DoFn methods

A [`DoFn`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.DoFn)
can be customized with a number of methods that can help create more complex behaviors.
You can customize what a worker does when it starts and shuts down with `setup` and `teardown`.
You can also customize what to do when a
[_bundle of elements_](/documentation/runtime/model/#bundling-and-persistence)
starts and finishes with `start_bundle` and `finish_bundle`.

- [`DoFn.setup()`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.DoFn.setup):
  Called whenever the `DoFn` instance is deserialized on the worker. This means it can be called more than once per worker because
  multiple instances of a given `DoFn` subclass may be created (e.g., due to parallelization, or due to garbage collection after a period
  of disuse).
  This is a good place to connect to database instances, open network connections or other resources.
  See also `DoFn.SetupContextParam` for a way to accomplish this via context managers.
- [`DoFn.start_bundle()`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.DoFn.start_bundle):
  Called _once per bundle of elements_ before calling `process` on the first element of the bundle.
  This is a good place to start keeping track of the bundle elements.
  See also `DoFn.BundleContextParam` for a way to accomplish this via context managers.
- [**`DoFn.process(element, \*args, **kwargs)`\*\*](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.DoFn.process):
  Called _once per element_, can _yield zero or more elements_.
  Additional `*args` or `**kwargs` can be passed through
  [`beam.ParDo()`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.ParDo).
  **[required]**
- [`DoFn.finish_bundle()`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.DoFn.finish_bundle):
  Called _once per bundle of elements_ after calling `process` after the last element of the bundle,
  can _yield zero or more elements_. This is a good place to do batch calls on a bundle of elements,
  such as running a database query.

  For example, you can initialize a batch in `start_bundle`,
  add elements to the batch in `process` instead of yielding them,
  then running a batch query on those elements on `finish_bundle`, and yielding all the results.

  Note that yielded elements from `finish_bundle` must be of the type
  [`apache_beam.utils.windowed_value.WindowedValue`](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/utils/windowed_value.py).
  You need to provide a timestamp as a unix timestamp, which you can get from the relevant processed elements.
  You also need to provide a window, which you can get from the relevant processed elements like in the example below.

- [`DoFn.teardown()`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.DoFn.teardown):
  Called _once (as a best effort) per `DoFn` instance_ when the `DoFn` instance is shutting down.
  This is a good place to close database instances, close network connections or other resources.

  Note that `teardown` is called as a _best effort_ and is _not guaranteed_.
  For example, if the worker crashes, `teardown` might not be called.

> _Known issues:_
>
> - [[Issue 19394]](https://github.com/apache/beam/issues/19394)
>   `DoFn.teardown()` metrics are lost.

## Related transforms

- [Map](/documentation/transforms/python/elementwise/map) behaves the same, but produces exactly one output for each input.
- [FlatMap](/documentation/transforms/python/elementwise/flatmap) behaves the same as `Map`,
  but for each input it may produce zero or more outputs.
- [Filter](/documentation/transforms/python/elementwise/filter) is useful if the function is just
  deciding whether to output an element or not.

[Pydoc Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.Pardo) |
