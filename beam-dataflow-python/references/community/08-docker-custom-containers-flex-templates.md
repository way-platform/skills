# Dataflow Python: Docker, Custom Containers & Flex Templates

In 2025+, deploying Dataflow pipelines directly from a local machine using `setup.py` is an anti-pattern. The modern, production-grade standard relies entirely on **Docker-based deployments** using Custom Containers and Flex Templates.

## Why Docker?
*   **Dependency Hell is Over:** Python dependency conflicts (especially with C-extensions like Pandas or NumPy) are eliminated when you pre-build the environment into a Docker image.
*   **Faster Worker Startup:** Instead of workers downloading packages via pip on startup (which takes minutes and can fail due to network blips), workers pull a pre-built image, starting almost instantly.
*   **Security & Compliance:** Security teams can scan the Docker image for vulnerabilities before it is deployed to production.

## Part 1: Custom SDK Containers
You can provide your own Docker image for Dataflow workers to execute your Python code.

1.  **The Dockerfile:** Base it on the official Google Dataflow Python image.
    ```dockerfile
    FROM apache/beam_python3.10_sdk:2.55.0

    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Copy your pipeline code
    COPY my_pipeline/ ./my_pipeline/
    ```
2.  **Usage:** Build, push to Artifact Registry, and pass `--sdk_container_image` when running your pipeline.

## Part 2: Flex Templates
Flex Templates take Dockerization a step further by packaging *both* the dependencies *and* the pipeline launch code. This separates developers from operators.

1.  **How it Works:** You build a Docker image containing your code. You register a `metadata.json` file in GCS that points to the image and defines expected parameters.
2.  **Execution:** Operators, CI/CD pipelines, or Cloud Composer trigger the job via an API call, passing runtime parameters without needing Python installed.

## Operations Best Practices
*   **CI/CD Pipeline:** Use Cloud Build or GitHub Actions to build the Docker image and stage the Flex Template metadata automatically on merge to the `main` branch.
*   **Version Control:** Tag your Docker images with Git commit SHAs, never just `latest`. Pass this specific tag to your Flex Template.
*   **Pre-bake External Binaries:** If your pipeline requires external Linux binaries (like a specialized audio processing tool), install them directly into the Dockerfile.

## References & Further Reading
*   [Google Cloud: Using Custom Containers](https://cloud.google.com/dataflow/docs/guides/using-custom-containers)
*   [Google Cloud: Flex Templates Documentation](https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates)
