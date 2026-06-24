# Retry policy reload rehearsal

During rollback rehearsal:

- Capture the current retry policy.
- Reload the workspace policy once.
- Confirm queued work retains its recorded retry budget.
- Confirm newly queued work reads the reloaded policy.

These are release rehearsal notes only.
No queue behavior changes in this update.
