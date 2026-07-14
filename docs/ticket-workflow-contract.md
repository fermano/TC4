# Delivery workflow contract

Delivery owner keys are trimmed and lowercased. Blank owners use `engineering-ops`.

Record filters preserve the input record order. A missing owner selection means no filtering. An explicitly empty owner selection selects no owners and returns no records.

Delivery summaries expose owner and status. Source metadata may be added as an opt-in field; behavior for blank or missing source values is not yet recorded here.
