---
source_url: https://beam.apache.org/documentation/io/built-in/webapis/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Web Apis I/O connector"
beam_last_updated: "Last updated on 2026/03/06"
---

[Built-in I/O Transforms](/documentation/io/built-in/)

# Web APIs I/O connector

The Beam SDKs include a built-in transform, called RequestResponseIO to support reads and writes with Web APIs such as
REST or gRPC.

Discussion below focuses on the Java SDK. Python examples will be added in the future; see tracker issue:
[#30422](https://github.com/apache/beam/issues/30422). Additionally, support for the Go SDK is not yet available;
see tracker issue: [#30423](https://github.com/apache/beam/issues/30423).

## RequestResponseIO Features

Features this transform provides include:

- developers provide minimal code that invokes Web API endpoint
- delegate to the transform to handle request retries and exponential backoff
- optional caching of request and response associations
- optional metrics

This guide currently focuses on the first two bullet points above, the minimal code requirements and error handling.
In the future, it may be expanded to show examples of additional features. Links to additional resources is
provided below.

## Additional resources

- [RequestResponseIO source code](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/io/requestresponse.py)
- [RequestResponseIO Pydoc](https://beam.apache.org/releases/pydoc/current/apache_beam.io.requestresponse.html)

## Before you start

## RequestResponseIO basics

### Minimal code

The minimal code needed to read from or write to Web APIs is:

1. Caller implementation.
2. Instantiate [RequestResponseIO](https://beam.apache.org/releases/pydoc/current/apache_beam.io.requestresponse.html#apache_beam.io.requestresponse.RequestResponseIO).

#### Implementing the Caller

Caller requires only one method override: \_\_call\_\_, whose
purpose is to interact with the API, converting a request into a response.
The transform’s DoFn invokes this method within its
[DoFn.process](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.DoFn.process)
method. The transform handles everything else including repeating failed requests and exponential backoff
(discussed more below).

![](/images/copy-icon.svg)

```
// MyCaller invokes a Web API with MyRequest and returns the resulting MyResponse.
class MyCaller(Caller):

    def __call__(self, request: Request):

        // Do something with request and return the response.
```

#### Instantiate RequestResponseIO

The `RequestResponseIO` transform returns a [Result](https://beam.apache.org/releases/javadoc/current/org/apache/beam/io/requestresponse/Result.html)
that bundles any failures and the `PCollection` of successful responses. In Beam, we call this the
[additional outputs](/documentation/programming-guide/#additional-outputs) pattern,
which typically requires a bit of boilerplate but the transform takes care of it for you. Using the transform,
you get the success and failure `PCollection`s via
[Result::getFailures](https://beam.apache.org/releases/javadoc/current/org/apache/beam/io/requestresponse/Result.html#getFailures--)
and [Result::getResponses](https://beam.apache.org/releases/javadoc/current/org/apache/beam/io/requestresponse/Result.html#getResponses--).

Below shows an abbreviated snippet how the transform may work in your pipeline.

Using [RequestResponseIO](https://beam.apache.org/releases/pydoc/current/apache_beam.io.requestresponse.html#apache_beam.io.requestresponse.RequestResponseIO)
is as simple as shown below. As mentioned, it minimally requires the `Caller`.

Below shows an abbreviated snippet how the transform may work in your pipeline.

![](/images/copy-icon.svg)

```
responses = requests | RequestResponseIO(MyCaller())
```

`RequestResponseIO` takes care of everything else needed to invoke the `Caller` for each request. It doesn’t care what
you do inside your `Caller`, whether you make raw HTTP calls or use client code. Later this guide discusses the
advantage of this design for testing.

### API call repeats and failures

This section provides a little more detail about handling failures and specifics on API call repeats with backoff.

#### Handling failures

The failures are an
[ApiIOError](https://beam.apache.org/releases/javadoc/current/org/apache/beam/io/requestresponse/ApiIOError.html)
`PCollection` that you may apply to a logging transform or a transform that
saves the errors to a downstream sink for later analysis and troubleshooting.

Since `ApiIOError` is already mapped to a Beam Schema, it has compatibility with most of Beam’s existing I/O
connectors.
(_Note: If the concept of Beam Schemas is new to you, please see the
[Beam Programming Guide](/documentation/programming-guide/#schemas)._)
For example, you can easily send `ApiIOError` records to BigQuery for analysis and troubleshooting as shown
below **without** converting the records first to a
[TableRow](https://www.javadoc.io/doc/com.google.apis/google-api-services-bigquery/v2-rev20230812-2.0.0/com/google/api/services/bigquery/model/TableRow.html).

I/O errors are retried by the PTransform if the Caller is raising certain errors.

#### API call repeats and backoff

Prior to emitting to the failure `PCollection`, the transform performs a retry **for certain errors**
after a prescribed exponential backoff. Your `Caller` must throw specific errors, to signal the transform
to perform the retry with backoff. Throwing a
[UserCodeExecutionException](https://beam.apache.org/releases/javadoc/current/org/apache/beam/io/requestresponse/UserCodeExecutionException.html)
will immediately emit the error into the `ApiIOError` `PCollection`.

`RequestResponseIO` will attempt a retry with backoff when `Caller` throws:

- [UserCodeQuotaException](https://beam.apache.org/releases/javadoc/current/org/apache/beam/io/requestresponse/UserCodeQuotaException.html)
- [UserCodeRemoteSystemException](https://beam.apache.org/releases/javadoc/current/org/apache/beam/io/requestresponse/UserCodeRemoteSystemException.html)
- [UserCodeTimeoutException](https://beam.apache.org/releases/javadoc/current/org/apache/beam/io/requestresponse/UserCodeTimeoutException.html)

After a threshold number of retries, the error is emitted into the failure `PCollection`.

Prior to raising an exception, the transform performs a retry **for certain errors**
using a prescribed exponential backoff. Your `Caller` must raise specific errors, to signal the transform
to perform the retry with backoff.

`RequestResponseIO` will attempt a retry with backoff when `Caller` raises:

- UserCodeQuotaException
- UserCodeTimeoutException

After a threshold number of retries, the error is re-raised.

#### Testing

Since `RequestResponseIO` doesn’t care what you do inside your `Caller` implementation, this makes some testing more convenient.
Instead of relying on direct calls to a real API within some tests, consequently depending on your external resource,
you simply implement a version of your `Caller`
returning responses or throwing exceptions, according to your test logic.
For example, if you want to test a downstream step in your pipeline for a specific response, say empty records, you
could easily do so via the following. For more information on testing your Beam Pipelines, see
the [Beam Programming Guide](/documentation/pipelines/test-your-pipeline/).

![](/images/copy-icon.svg)

```
def test_empty_response():
    // Test expects PTransform underTest should do something as a result of empty records, for example.
    with TestPipeline() as p:
        responses = (
            p
            | beam.Create("aRequest")
            | beam.RequestResponseIO(MockEmptyIterableResponse())
        )
        assert_that(responses, equal_to(...))
}

// MockEmptyIterableResponse simulates when there are no results from the API.
class MockEmptyIterableResponse(Caller):
    def __call__(self, request: str):
        return []
```

## Practical examples

Below shows two examples that we will bring together in an end-to-end Beam pipeline. The goal of this pipeline is to
download images and use
[Gemini on Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart-multimodal)
to recognize the image content.

Note that this example does not replace our current AI/ML solutions. Please see
[Get started with AI/ML pipelines](/documentation/ml/overview/)
for more details on using Beam with AI/ML.

### Working with HTTP calls directly

We first need to download images. To do so, we need to make HTTP calls to the image URL and emit their content
into a `PCollection` for use with the Gemini API. The value of this example on its own is that it demonstrates
how to use `RequestResponseIO` to make raw HTTP requests.

#### Define Caller

We implement the `Caller`, the `HttpImageClient`, that receives an `ImageRequest` and returns an `ImageResponse`.

_For demo purposes, the example uses a tuple to preserve the raw URL in the returned `ImageResponse`._

##### Abbreviated snippet

Below shows an abbreviated version of the `HttpImageClient` showing the important parts.

![](/images/copy-icon.svg)

```
class HttpImageClient(Caller):

    def __call__(self, request: ImageRequest):
        response = requests.get(ImageRequest.url);
        return ImageResponse(request.mime_type, response.content)
    }

}
```

##### Full example

The full implementation is shown below illustrating throwing various exceptions based on the HTTP response code.

![](/images/copy-icon.svg)

```
class HttpImageClient(Caller):
    STATUS_TOO_MANY_REQUESTS = 429
    STATUS_TIMEOUT = 408

    def __call__(self, kv):
        url, request = kv
        try:
            response = requests.get(request.image_url)
        except requests.exceptions.Timeout as e:
            raise UserCodeTimeoutException() from e
        except requests.exceptions.HTTPError as e:
            raise UserCodeExecutionException() from e

        if response.status_code >= 500:
            raise UserCodeExecutionException()

        if response.status_code >= 400:
            match response.status_code:
                case self.STATUS_TOO_MANY_REQUESTS:
                    raise UserCodeQuotaException()
                case self.STATUS_TIMEOUT:
                    raise UserCodeTimeoutException()
                case _:
                    raise UserCodeExecutionException()

        return url, ImageResponse(request.mime_type, response.content)
```

#### Define request

`ImageRequest` is the custom request we provide the `HttpImageClient`, defined in the example above, to invoke the HTTP call
that acquires the image.

![](/images/copy-icon.svg)

```
class ImageRequest:
    image_url_to_mime_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
    }

    def __init__(self, image_url):
        self.image_url = image_url
        self.mime_type = self.image_url_to_mime_type.get(image_url.split(".")[-1])
```

#### Define response

`ImageResponse` is the custom response we return from the `HttpImageClient`, defined in the example above, that contains the image data
as a result of calling the remote server with the image URL.

![](/images/copy-icon.svg)

```
ImageResponse = namedtuple("ImageResponse", ["mime_type", "data"])
```

#### Define response coder

#### Acquire image data from URLs

Below shows an example how to bring everything together in an end-to-end pipeline. From a list of image URLs,
the example builds the `PCollection` of `ImageRequest`s that is applied to an instantiated `RequestResponseIO`,
using the `HttpImageClient` `Caller` implementation.

![](/images/copy-icon.svg)

```
def what_is_this_image_http(options):
    images = [
        "https://storage.googleapis.com/generativeai-downloads/images/cake.jpg",
        "https://storage.googleapis.com/generativeai-downloads/images/chocolate.png",
        "https://storage.googleapis.com/generativeai-downloads/images/croissant.jpg",
        "https://storage.googleapis.com/generativeai-downloads/images/dog_form.jpg",
        "https://storage.googleapis.com/generativeai-downloads/images/factory.png",
        "https://storage.googleapis.com/generativeai-downloads/images/scones.jpg",
    ]

    with beam.Pipeline(options=options) as pipeline:
        _ = (
            pipeline
            | "Create data" >> beam.Create(images)
            | "Map to ImageRequest" >> beam.Map(lambda url: ImageRequest(url))
            | "Download image" >> RequestResponseIO(HttpClient())
            | "Print results"
            >> beam.Map(
                lambda response: print(
                    f"mimeType={response.mime_type}, size={len(response.data)}"
                )
            )
        )
```

The pipeline output, shown below, displays a summary of the downloaded image, its URL, mimetype and size.

![](/images/copy-icon.svg)

```
https://storage.googleapis.com/generativeai-downloads/images/factory.png, mimeType=image/png, size=23130
https://storage.googleapis.com/generativeai-downloads/images/scones.jpg, mimeType=image/jpeg, size=394671
https://storage.googleapis.com/generativeai-downloads/images/cake.jpg, mimeType=image/jpeg, size=253809
https://storage.googleapis.com/generativeai-downloads/images/chocolate.png, mimeType=image/png, size=29375
https://storage.googleapis.com/generativeai-downloads/images/croissant.jpg, mimeType=image/jpeg, size=207281
https://storage.googleapis.com/generativeai-downloads/images/dog_form.jpg, mimeType=image/jpeg, size=1121752
```

### Using API client code

The last example demonstrated invoking HTTP requests directly. However, there are some API services that provide
client code that one should use within the `Caller` implementation. Using client code within Beam presents
unique challenges, namely serialization. Additionally, some client code requires explicit handling in terms of
setup and teardown.

`RequestResponseIO` can handle an additional interface called `SetupTeardown` for these scenarios.

The [SetupTeardown](https://beam.apache.org/releases/javadoc/current/org/apache/beam/io/requestresponse/SetupTeardown.html)
interface has only two methods, setup and teardown.

`RequestResponseIO` can handle such setup and teardown scenarios by overwriting context manager dunder methods
**enter** and **exit** on the Caller.

The transform also handles retries with backoff, likewise dependent on the thrown Exception, as discussed previously
in this guide.

#### Define Caller with SetupTeardown

Below is
an example that adapts
[Vertex AI Gemini Java Client](https://cloud.google.com/vertex-ai/docs/generative-ai/start/quickstarts/quickstart-multimodal)
to work in a Beam pipeline using `RequestResponseIO`, adding usage of the `SetupTeardown` interface,
in addition to the required `Caller`. It has a bit more boilerplate than the simple HTTP example above.

##### Abbreviated snippet

An abbreviated snippet showing the important parts is shown below.

##### Full example

![](/images/copy-icon.svg)

```
class GeminiAIClient(Caller):
    MODEL_GEMINI_FLASH_LITE = "gemini-2.0-flash-lite"

    def __init__(self, api_key):
        self.api_key = api_key

    def __enter__(self):
        self.client = genai.Client(api_key=self.api_key)
        return self

    def __call__(self, kv):
        url, request = kv
        try:
            response = self.client.models.generate_content(
                model=self.MODEL_GEMINI_FLASH_LITE,
                contents=[
                    types.Part.from_bytes(
                        data=request.data,
                        mime_type=request.mime_type,
                    ),
                    "Caption this image.",
                ],
            )
        except APIError as e:
            raise UserCodeExecutionException() from e

        return url, response
```

#### Ask Gemini AI to identify the image

Now let’s combine the previous example of acquiring an image to this Gemini AI client to ask it to identify the image.

Below is what we saw previously but encapsulated in a convenience method. It takes a `List` of urls, and returns
a `PCollection` of `ImageResponse`s containing the image data.

Next we convert the `ImageResponse`s into a `PCollection` of `GenerateContentRequest`s.

Finally, we apply the `PCollection` of `ImageResponse`s to `RequestResponseIO`, instantiated using the
`genai.Client`, defined above.

The full end-to-end pipeline is shown below.

![](/images/copy-icon.svg)

```
def what_is_this_image_gemini(options):
    images = [
        "https://storage.googleapis.com/generativeai-downloads/images/cake.jpg",
        "https://storage.googleapis.com/generativeai-downloads/images/chocolate.png",
        "https://storage.googleapis.com/generativeai-downloads/images/croissant.jpg",
        "https://storage.googleapis.com/generativeai-downloads/images/dog_form.jpg",
        "https://storage.googleapis.com/generativeai-downloads/images/factory.png",
        "https://storage.googleapis.com/generativeai-downloads/images/scones.jpg",
    ]

    with beam.Pipeline(options=options) as pipeline:
        _ = (
            pipeline
            | "Create data" >> beam.Create(images)
            | "Map to ImageRequest" >> beam.Map(build_image_request)
            | "Download image" >> RequestResponseIO(HttpClient())
            | "Gemini AI" >> RequestResponseIO(GeminiAIClient(API_KEY))
            | "Print results" >> beam.Map(lambda response: print(response.text))
        )
```

Below shows an abbreviated output of running the full pipeline, where we see the result of Gemini AI identifying the images.

![](/images/copy-icon.svg)

```
https://storage.googleapis.com/generativeai-downloads/images/cake.jpg Here are some caption ideas for the image:

**Short & Sweet:**

*   Tiramisu perfection.
*   Dessert dreams.
*   A slice of heaven.

**Descriptive:**

*   Layers of creamy tiramisu, dusted with cocoa and drizzled with chocolate, a perfect treat.
*   A beautifully presented tiramisu slice on a white plate, ready to be savored.
*   Indulge in this classic Italian dessert.

**Playful:**

*   "Life is what you bake it." - with this dessert!
*   I'd share, but...
*   This tiramisu is calling my name.

**If you want to be more specific, tell me:**

*   Who might see this? (e.g., food bloggers, friends on social media)
*   What mood are you going for? (e.g., elegant, fun, hungry)
*   Where is this image from? (e.g., a restaurant, your kitchen)

I can tailor a caption just for you!

https://storage.googleapis.com/generativeai-downloads/images/chocolate.png Here are some captions for the image:

*   "Chocolate is always a good idea."
*   "Time for a sweet treat!"
*   "Unwrapping happiness."
*   "Chocolate bar emoji, yum!"
*   "Can't resist a good chocolate bar."
https://storage.googleapis.com/generativeai-downloads/images/croissant.jpg Here are some captions for the image of croissants:

**Short & Sweet:**

*   Freshly baked bliss.
*   Croissant cravings.
*   Golden and flaky.
*   Breakfast goals.
*   Morning perfection.

**Descriptive:**

*   A basket overflowing with buttery, golden croissants.
*   Close-up shot of a pile of freshly baked croissants, perfect for a morning treat.
*   The irresistible aroma of warm croissants, ready to be enjoyed.
*   Delicious, flaky croissants in a woven basket.

**Playful:**

*   Warning: May cause intense croissant cravings.
*   My love language: croissants.
*   Life is better with a croissant in hand.
*   Just a few croissantsâ¦ whatâs the worst that could happen?

**If you want me to generate more, just tell me what you'd like to focus on (e.g., a specific feeling, occasion, etc.)!**
```
