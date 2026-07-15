# Delivery workflow contract

Delivery owner keys are trimmed and lowercased, and internal whitespace runs are collapsed to a single space. Blank owners use `engineering-ops`.

Record filters preserve the input record order. A missing owner selection means no filtering. An explicitly empty owner selection selects no owners and returns no records.

Delivery summaries expose owner and status. Source metadata is available as an opt-in field; blank or missing source values are reported as `unknown`.
