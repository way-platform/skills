---
source_url: https://docs.cloud.google.com/dataflow/docs/cuds
fetched_at_utc: 2026-03-07T13:02:33.404041+00:00
page_title: "Committed use discounts \u00a0|\u00a0 Cloud Dataflow \u00a0|\u00a0 Google Cloud Documentation"
last_updated: "Last updated 2026-03-03 UTC."
---

This document describes spend-based committed use discounts (CUDs) for Dataflow.

Committed use discounts (CUDs) for Dataflow provide
discounted prices in exchange for your commitment to continuously spend a
minimum hourly amount on Dataflow capacity for a year or longer.

Dataflow spend-based CUDs are ideal when your spending on
Dataflow capacity involves a predictable minimum that you can
commit to for at least a year.

**Important:** This page explains the new and improved committed use discounts (CUDs) program,
which applies to any customers who purchase their first CUDs on or after
**July 15, 2025**. For more information, see
[Spend-based CUDs program improvements](/docs/cuds-multiprice).

## Dataflow CUD pricing

Dataflow CUDs offer two levels of discounts, depending on the commitment period:

- **20% discount**: You get this by committing to a 1-year term. For the duration of your term, you pay the Dataflow CUD 1-year price (consumption model ID 75D9-38E7-870F) as your committed hourly spend amount.
- **40% discount**: You get this by committing to a 3-year term. For the duration of your term, you pay the Dataflow CUD 3-year price (consumption model ID 9E06-4EF0-37D8) as your committed hourly spend amount.

When you purchase a commitment, you agree to pay a fixed hourly fee for a one
or three-year term. Your monthly invoice shows usage charges using the
CUD [consumption model](/billing/docs/resources/multiprice-cuds)
prices for usage that falls within your commitment. You're charged $1 for
$1 worth of commitment fees, and a corresponding credit applies so that the
commitment fee is offset for any utilized portion of your commitment.
For a full example, see
[An example Dataflow CUD](#example).

For any unused portion of your commitment, the fee applies. The result
is that you pay the flat commitment fee every hour, whether you use the
services or not, but commitment fees are then credited back to you for the
used portions within the commitment amount.

Any expenditure beyond the commitment gets billed at the on-demand rate.
As your usage grows, you can purchase additional commitments to receive
discounts on increased expenditures not covered by previous commitments.

The CUD discount applies to any eligible usage in projects
associated with the Cloud Billing account.

If the on-demand rates change after you purchase a commitment,
your commitment fee doesn't change.

The discount applies to any eligible usage in Dataflow projects
associated with the Cloud Billing account used to purchase the commitment,
regardless of instance configuration or region. All CUDs apply to both regional
and multi-region configurations.

## Resources eligible for Dataflow CUDs

**Note:** While Dataflow Committed Use Discounts (CUDs) don't apply to
GPUs and TPUs, you can apply resource-based CUDs for these accelerators by
purchasing Compute Engine [resource-based commitments](/compute/docs/instances/signing-up-committed-use-discounts)
with _specifically targeted_ reservations, and using these reservations
with Dataflow. For more
information, see [Use Compute Engine reservations with
Dataflow](/dataflow/docs/guides/compute-engine-reservations).

Dataflow committed use discounts automatically apply to your
spending on the Dataflow compute capacity used by streaming jobs
across projects. This flexibility helps you achieve a high utilization rate of
your commitment across regions and projects without manual intervention, saving
you time and money. Dataflow CUDs apply to your spending on the
following resources:

- Worker CPU and memory for streaming jobs
- Streaming Engine data processed
- Streaming Engine compute units
- Data Compute Units (DCUs) for Dataflow Prime streaming jobs

Dataflow CUDs don't apply to your spending on the following resources:

- Worker CPU and memory for batch and FlexRS jobs
- Dataflow Shuffle data processed
- Data Compute Units (DCUs) for Dataflow Prime batch jobs
- Persistent Disk storage
- GPUs and TPUs
- Snapshots
- Confidential VMs

For a list of applicable SKUs, see [Dataflow CUD Eligible SKUs](/skus/sku-groups/dataflow-cud-eligible-skus).

## Purchase a Dataflow commitment

After your purchase a CUD, you can't cancel your commitment. Make sure the
size and duration of your commitment aligns with both your historical and your
expected minimum expenditure on Dataflow capacity. For more
information, see
[Canceling commitments](/docs/cuds-spend-based#canceling_commitments).

To purchase or manage Dataflow committed use discounts for your
Cloud Billing account, follow the instructions at
[Purchasing spend-based
commitments](/docs/cuds-spend-based#purchasing).

## An example Dataflow CUD scenario

Ideally, your commitment represents at least your expected minimum hourly
expenditure on Dataflow streaming jobs across your projects over
the next one or three years.

As an example, say that you run Dataflow streaming jobs in two
different regions: `us-central1` and `us-west2`.

The streaming job in `us-central1` uses the following resources:

- 10 nodes of instance type `n1-standard-1` (vCPUs: 1, RAM: 3.75 GB)
- 20 Streaming Engine Compute Units per hour

The streaming job in `us-west2` uses the following resources:

- 10 nodes of instance type `n1-standard-1` (vCPUs: 1, RAM: 3.75 GB)
- 20 Streaming Engine Compute Units per hour

**Note:** The prices in this section are examples. For current pricing, see the
[Dataflow Pricing](https://cloud.google.com/dataflow/pricing) page.

From the [pricing page](https://cloud.google.com/bigtable/pricing), see the price in the column labeled **1-year commitment** to calculate the approximate hourly commitment cost:

- Total expenditure in `us-central1` = $2.08271 per hour
  - 10 nodes \* 1 streaming vCPU per node \* $0.0552 per streaming vCPU per hour = $0.552 per hour
  - 10 nodes \* 3.75GB per node \* $0.0028456 per GB per hour = $0.10671 per hour
  - 20 Streaming Engine Compute Units \* $0.0712 per compute unit per hour = $1.424 per hour
- Total expenditure in `us-west2`= $2.5024 per hour
  - 10 nodes \* 1 streaming vCPU per node \* $0.06624 per streaming vCPU per hour = $0.6624 per hour
  - 10 nodes \* 3.75GB per node \* $0.00341472 per GB per hour = $0.128 per hour
  - 20 Streaming Engine Compute Units \* $0.0856 per compute unit per hour = $1.712 per hour
- Total expenditure across all regions = $4.585 per hour

If you expect to spend that minimum of $4.585 per hour continuously for the next
year or more, then you can make a commitment for that amount. When purchasing
the commitment, you enter `$4.585` as the hourly commitment amount.

In the legacy CUDs program, your commitment amount is the on-demand price instead. For more
information about the differences between the legacy and new spend-based CUDs program, see
[Spend-based CUDs program improvements](/docs/cuds-multiprice).

If you expect to scale down your clusters sometimes, you can make a commitment
for a lower amount. Any expenditure above the commitment amount is charged at
the on-demand rate.

As a basis for comparison, compute the on-demand cost of Dataflow capacity, without the application of any commitment discounts:

- Monthly cost based on on-demand pricing: $5.73 per hour \* 730 hours = $4,182.9 per month.

From here, you can calculate the monthly costs and savings that you would see
under a one-year commitment with a 20% discount compared to a year of paying the
full rates:

- Monthly cost of a one-year, $4.585/hour commitment \* 730 hours = $3,346.32 per month
- Total savings per month: $4,182.90 - $3,346.32 = $836.58
- Total savings with a one-year, $5.73/hour commitment: $836.58 per month \* 12 months = **$10,038.96**

You can apply similar math to calculating the costs and savings of a three-year CUD, with its 40% discount compared to on-demand rates:

- Monthly cost of a three-year commitment: $3.438 per hour \* 730 hours = $2,509.74 per month
- Total savings per month: $4,182.90 - $2,509.74 = $1,673.16
- Total savings with a three-year, $5.73/hour CUD: $1,673.16 per month \* 36 months = **$60,233.76**

A commitment that covers your expected minimum Dataflow streaming
usage over the years to come can lead to significant savings.

## Recommendations for choosing a commitment

When considering the purchase of Dataflow CUDs, keep in mind
the following:

- **Projects**: Determine the consistent baseline expenditure per
  project while calculating total commitment. Consider that production
  loads usually run 100% of the time, while development or staging
  environments might run intermittently.
- **Resources**: If you frequently scale your resources up or
  down, consider purchasing CUDs only for their baseline predictable usage.
  If you have instances that you run only for bursts or brief durations, exclude
  them from your calculations.

Your commitment fee applies to every hour during the term of the
commitment, regardless of actual usage. Choose your CUD's commitment
amount carefully, based on both your historical Dataflow usage
and your future expectations. As long as your use of Dataflow
capacity stays higher than your committed expenditure level, you will
enjoy the maximum possible discount for the length of that commitment.

## What's next

- Read [an overview of Dataflow pricing](https://cloud.google.com/dataflow/pricing).
- Learn [more about Google Cloud Platform spend-based CUDs](/docs/cuds).
- Learn how to [view your CUD reports](/billing/docs/how-to/cud-analysis).
- Understand savings with [cost breakdown reports](/billing/docs/how-to/cost-breakdown).
