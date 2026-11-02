# Healthcare analytics code review checklist

## Correctness
- Is row grain stated for every input and output?
- Can joins multiply rows? Is cardinality checked before/after?
- Are numerator, denominator, cohort, date boundaries and exclusions explicit?
- Are NULLs and unknown categories handled transparently?
- Are duplicate candidates reviewed rather than automatically deleted?
- Are units, ranges, timezone and chronology validated?
- Are calculations independently reconciled?

## Healthcare interpretation
- Is an order distinguished from administration, dispensing and adherence?
- Is a claims availability proxy distinguished from ingestion?
- Are supplied outcomes and flags validated before use?
- Are association, prediction and causation kept distinct?
- Are guideline claims tied to a dated source and applicable criteria?
- Are small cells and privacy risks considered?

## Engineering
- Is the code modular and readable?
- Are paths portable and secrets absent?
- Are tests deterministic and useful?
- Can a new user reproduce the result from documented steps?
- Are dependencies pinned or bounded and version recorded?
- Are logs and failures visible?

## Communication
- Does the output answer the original decision question?
- Are findings stated with denominators and time periods?
- Are limitations and unresolved issues prominent?
- Is the handoff clear enough for another analyst to continue?
