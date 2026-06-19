# Export alert retry example

Example payload:

{"status": "delayed", "workspace": "ws-204", "retry_count": 2, "attempt_type": "retry"}

The runbook treats retry_count 0 as the initial attempt.
