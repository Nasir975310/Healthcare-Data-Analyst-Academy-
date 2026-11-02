# Client assignment: Department medication utilisation review

**Time limit:** 90 minutes. **Audience:** Hospital quality and pharmacy operations team.

The client requests a reproducible database extract for a monthly review. Use the supplied synthetic training database only.

## Required outputs
1. Department summary: encounter count, mean length of stay, medication-order count.
2. Encounters with no medication orders.
3. Therapeutic-class order volume and rank.
4. Data-quality audit: duplicate primary keys, orphan references, invalid chronology and missing unit cost.
5. A short handoff explaining grain, denominator, date scope, exclusions, limitations and recommended next checks.

## Acceptance rules
- State that order rows represent orders, not administrations, dispensing, adherence or clinical exposure.
- Keep encounter-level denominators separate from order-level denominators.
- Preserve zero-order encounters in the exception output.
- Do not call the supplied 30-day flag a validated readmission outcome.
- Do not infer clinical appropriateness from utilisation volume alone.
- Provide SQL source and reproducible row counts.
