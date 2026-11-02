# Synthetic Antihypertensive Utilisation Review

## Executive summary
This training project describes order-level antihypertensive patterns in a synthetic dataset. It does not estimate actual hospital prescribing quality or clinical effectiveness.

## Business question
What generic-name and therapeutic-class order patterns are present in the supplied synthetic extract, and what data-quality limitations affect interpretation?

## Data and grain
One row per synthetic medication order line. Order lines do not demonstrate administration, dispensing or adherence.

## Method
Profile keys and missingness, filter the declared class, summarise order lines and quantity by generic name, and report missing unit cost separately.

## Validation
Confirm unique order IDs, reconcile source row counts, inspect missing costs and orphan encounter references, and independently recompute at least one summary.

## Limitations
Synthetic data, incomplete clinical context, no validated dose/route appropriateness criteria, no administration data and no patient-level causal inference.
