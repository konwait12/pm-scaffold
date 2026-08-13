# Audit Checklist · Tracking Plan

## Structural Gate

- All required headings exist (§1-§8 + `## Constitution Compliance`).
- Every event has a stable ID (`EV-NNN`), `event_name`, `event_type`, FUN/IX/BR reference, trigger condition, properties, upload timing, platform, metric, goal, and priority.
- Every event links to a FUN-XXX and a G-X — no orphan events.
- Material claims reference upstream artifact IDs. Blocking questions are marked explicitly.

## Coverage Gate

- Every P0 FUN-XXX has at least one `must_track` event (coverage matrix hard constraint).
- The coverage matrix status column shows no `⚠️ 待补` for P0 functions at `ready_for_sub_skill_review`.
- Every G-X that must be measurable after launch has the events + properties needed to verify it.

## Event Schema Gate

- `event_name` is snake_case verb_noun and globally unique; no duplicate-meaning events under different names.
- `event_type` is one of the allowed set (`page_view` / `click` / `submit` / `exposure` / `success` / `error` / `custom`).
- `upload_timing` is one of `realtime` / `near_realtime` / `batch` / `on_session_end` and matches the metric's needs.
- `platform` is one of `web` / `ios` / `android` / `miniprogram` / `server`.

## PII Gate

- Every property has a `pii_flag`: `false` / `quasi` / `true` / `sensitive`.
- PII/sensitive events carry an explicit data-retention rule in `notes`.
- No silent collection of identifiers, fingerprints, or sensitive content without flags.

## Metric Gate

- Every `must_track` event maps to a goal (G-X) and a metric type.
- Metrics are traceable to background-goal targets; the plan does not invent numeric targets.

## Quality Lenses

- First principles: every event answers a real business question; no "track everything" noise.
- Adversarial review: at least one plausible misinterpretation of an event was tested.
- Reverse validation: walking back from each G-X, all needed events/properties exist.
- Minimal sufficiency: the event list contains what data/engineering need and excludes SQL/table design.

## Human Gate

Set `needs_user_input` when coverage fails, when a trigger/property is ambiguous, or when a PII decision changes the contract.

Set `conditional_review` only when remaining unknowns are non-blocking, have owners, and include deferral risks.

Set `ready_for_sub_skill_review` only when all other gates pass. Never set `confirmed`; only the metric/data owner plus the function-description parent Skill may do so.

## Audit Report Shape

```text
status_recommendation
passed_checks
failed_checks
repairs_applied
must_track_count
nice_to_track_count
pii_event_count
unmapped_events
blocking_questions
downstream_risks
```
