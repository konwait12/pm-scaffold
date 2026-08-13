# Human Gate And Revision Loop

Every main work item stops after Audit. The authorized human chooses `approve` or `changes`; skipping is not approval.

On changes: record added/modified/removed content and downstream impact, update the candidate, rerun Audit, and resubmit. Three repeated failures on the same issue trigger a direction review rather than another blind edit. Ten total revision rounds block the item for owner escalation.

Only `pipeline.py ... review --decision approve --reviewer <name>` may create a confirmed baseline. Non-interactive mode and simulated identities cannot approve.
