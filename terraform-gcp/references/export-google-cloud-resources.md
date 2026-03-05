# Export your Google Cloud resources to Terraform format

**Preview**

This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the [Service Specific Terms](https://docs.cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is" and might have limited support. For more information, see the [launch stage descriptions](https://cloud.google.com/products/#product-launch-stages).

**Caution:** This feature isn't supported on Windows operating systems.

You've deployed resources in Google Cloud, and now need to manage your infrastructure as code (IaC) with Terraform. Google provides a tool that you can use to generate Terraform code for resources in a project, folder, or organization.

## Roles

To get the permissions that you need to export assets to Terraform, ask your administrator to grant you the following IAM roles on the organization, folder, or project:

- [Service Usage Consumer](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage#serviceusage.serviceUsageConsumer) (`roles/serviceusage.serviceUsageConsumer`)
- If writing state to an existing bucket (`--storage-path=BUCKET`):
    - [Storage Object Creator](https://docs.cloud.google.com/iam/docs/roles-permissions/storage#storage.objectCreator) (`roles/storage.objectCreator`)
    - [Storage Object Viewer](https://docs.cloud.google.com/iam/docs/roles-permissions/storage#storage.objectViewer) (`roles/storage.objectViewer`)
- If writing state to a new bucket: [Storage Object Viewer](https://docs.cloud.google.com/iam/docs/roles-permissions/storage#storage.objectViewer) (`roles/storage.objectViewer`)

For more information about granting roles, see [Manage access to projects, folders, and organizations](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access).

You might also be able to get the required permissions through [custom roles](https://docs.cloud.google.com/iam/docs/creating-custom-roles) or other [predefined roles](https://docs.cloud.google.com/iam/docs/roles-overview#predefined).

## Before you begin

- Prepare Cloud Shell.
    
    Launch [Cloud Shell](https://shell.cloud.google.com/), and set the default Google Cloud project where you want to generate Terraform code for the deployed resources.
    
    You only need to run this command once per project, and you can run it in any directory.
    
    ```bash
    export GOOGLE_CLOUD_PROJECT=PROJECT_ID
    ```

    Environment variables are overridden if you set explicit values in a Terraform configuration file.
    
- In Cloud Shell, install the command-line interface (CLI) for Config Connector.
    
    ```bash
    gcloud components install config-connector
    ```

    Config Connector lets you use Google Cloud's Terraform bulk-export tool.

    If you see `ERROR: (gcloud.components.install) You cannot perform this action because the Google Cloud CLI component manager is disabled for this installation`, run the following command instead:

    ```bash
    sudo apt-get install google-cloud-sdk-config-connector
    ```
    
- Enable the Cloud Asset API.
    
    ```bash
    gcloud services enable cloudasset.googleapis.com
    ```

- Create a service account to use for this export:
    
    ```bash
    gcloud beta services identity create --service=cloudasset.googleapis.com
    ```
    
- Ensure that the [Cloud Asset Service Agent](https://docs.cloud.google.com/iam/docs/service-agents) (`gcp-sa-cloudasset.iam.gserviceaccount.com`) has the `roles/servicenetworking.serviceAgent` role:
    
    ```bash
    gcloud projects add-iam-policy-binding PROJECT_ID \
      --member=serviceAccount:service-PROJECT_NUMBER@gcp-sa-cloudasset.iam.gserviceaccount.com \
      --role=roles/servicenetworking.serviceAgent
    ```

- Ensure that the [Cloud Asset Service Agent](https://docs.cloud.google.com/iam/docs/service-agents) (`gcp-sa-cloudasset.iam.gserviceaccount.com`) has the `roles/storage.objectAdmin` role:
    
    ```bash
    gcloud projects add-iam-policy-binding PROJECT_ID \
      --member=serviceAccount:service-PROJECT_NUMBER@gcp-sa-cloudasset.iam.gserviceaccount.com \
      --role=roles/storage.objectAdmin
    ```

    **Note:** To get your `PROJECT_ID` and `PROJECT_NUMBER`, go to the [Google Cloud console](https://console.cloud.google.com/home/dashboard).

## Limitations

Some resource types aren't supported for export to Terraform format even though they are supported by the Terraform Google provider. For a list of resource types that are supported for export to Terraform format, run the [`gcloud beta resource-config list-resource-types`](https://docs.cloud.google.com/sdk/gcloud/reference/beta/resource-config/list-resource-types) command.

## Export the entire project configuration to Terraform HCL code

The [`gcloud beta resource-config bulk-export --resource-format=terraform`](https://docs.cloud.google.com/sdk/gcloud/reference/beta/resource-config/bulk-export) command exports resources configured in the project, folder, or organization and prints them to the screen in [HCL code format](https://www.terraform.io/language/configuration-0-11/syntax).

```bash
gcloud beta resource-config bulk-export \
  --project=PROJECT_ID \
  --resource-format=terraform
```

### Write the output to a directory structure

- If you haven't done so already, create the directory where you want to output the project's configuration:
    
    ```bash
    mkdir OUTPUT_DIRECTORY
    ```

- Export the project's entire configuration to the directory:
    
    ```bash
    gcloud beta resource-config bulk-export \
      --path=OUTPUT_DIRECTORY \
      --project=PROJECT_ID \
      --resource-format=terraform
    ```
    
    The `--path` flag specifies the location to output the HCL code.

After running the command, the HCL code for each resource is output to a separate `.tf` file in the following directory structure:

```text
OUTPUT_DIRECTORY/
└── projects/
    └── PROJECT_ID/
        └── RESOURCE_TYPE/
```

### Write the output to a single file

If you don't want to print the output to the screen or create separate `.tf` files, you can write all of the output to a single file, as shown in this example:

```bash
gcloud beta resource-config bulk-export \
  --resource-format=terraform \
  --project=PROJECT_ID \
  >> gcp_resources.tf
```

## Filter the output

Filter the output of the bulk export command by specifying resource types.

### List the supported resource types to filter on

For a list of resource types that are supported for export to Terraform format, run the [`gcloud beta resource-config list-resource-types`](https://docs.cloud.google.com/sdk/gcloud/reference/beta/resource-config/list-resource-types) command:

```bash
gcloud beta resource-config list-resource-types
```

Optionally, write the output to a file:

```bash
gcloud beta resource-config list-resource-types >> strings.txt
```

In the output, the resource type for Compute Engine VMs is listed as:

```text
KRM KIND: ComputeInstance
```

You can ignore the `KRM KIND:` prefix.

### Export a single resource type

Use a string, such as `ComputeInstance`, to export specific resource types for your project in HCL code format:

```bash
gcloud beta resource-config bulk-export \
  --resource-types=RESOURCE_TYPE \
  --project=PROJECT_ID \
  --resource-format=terraform
```

The `--resource-types` flag specifies the resource type to output.

### Export multiple resource types

Export VM instances and firewall rules in HCL code format:

```bash
gcloud beta resource-config bulk-export \
  --resource-types=ComputeFirewall,ComputeInstance \
  --project=PROJECT_ID \
  --resource-format=terraform
```

### Use a file to specify the resource types to export

- Create a directory called `tf-output`.
    
    ```bash
    cd && mkdir tf-output && cd tf-output
    ```

- Create a file called `types.txt`, and add a list of resource types. For example:
    
    ```text
    ComputeBackendBucket
    ComputeBackendService
    ComputeForwardingRule
    ```

- Run the `gcloud beta resource-config bulk-export` command with the `--resource-types-file` flag:
    
    ```bash
    gcloud beta resource-config bulk-export \
      --resource-types-file=types.txt \
      --path=tf-output \
      --project=PROJECT_ID \
      --resource-format=terraform
    ```

If the project doesn't contain any of a particular resource type, the command succeeds but nothing is output for that resource type.

## Troubleshooting

If you see the following error:

"Permission denied during export. Please ensure the Cloud Asset Inventory API is enabled."

Make sure that you have followed the instructions in the [Before you begin](https://docs.cloud.google.com/docs/terraform/resource-management/export#before-you-begin) section.