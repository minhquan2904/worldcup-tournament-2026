# Systematic Debugging — 4-Phase Investigation Framework

> ALWAYS find root cause. NEVER fix symptoms. Even if faster, even if urgent, even if obvious.

## Phase 1: Investigation (MANDATORY FIRST)
| Step | Action |
|------|--------|
| 1.1 | Read FULL error message (not just first line) |
| 1.2 | Read stack trace bottom→up, find OUR code (!framework) |
| 1.3 | Reproduce consistently (minimum steps) |
| 1.4 | Check recent changes: git log, git diff |
| 1.5 | Check environment: config, env variables, DB state |

⛔ !attempt fix before completing Phase 1
⛔ !assume — verify with evidence

## Phase 2: Pattern Analysis
| Step | Action |
|------|--------|
| 2.1 | Find working reference (similar code that works) |
| 2.2 | Compare side by side (diff broken vs working) |
| 2.3 | Check conventions (load convention checker sub-skill) |
| 2.4 | Review dependencies (who calls this? what does this call?) |

⛔ !claim understanding without completely reading code

## Phase 3: Hypothesis Formation
1. List 2-5 potential causes (from Phase 1+2)
2. Rank by likelihood (Occam's Razor, evidence-backed higher)
3. Pick TOP 1 hypothesis
4. Define prediction: "IF [hypothesis] correct, THEN [outcome] when [test]"
5. Test prediction → Confirm or Reject

⛔ Single hypothesis at a time. !test multiple parallel.
⛔ Each hypothesis MUST have specific prediction.
⛔ Rejected? → STOP → back to Phase 1/2 → NEW hypothesis. !stack fixes.

## Phase 4: Implementation
| Step | Action |
|------|--------|
| 4.1 | Write test reproducing bug (MUST fail — RED) |
| 4.2 | Implement MINIMUM change (test passes — GREEN) |
| 4.3 | Add edge case tests |
| 4.4 | Run existing tests (no regression) |
| 4.5 | Refactor AFTER green — SEPARATE commit |

⛔ >20 lines fix → verify hypothesis first
⛔ !refactor in fix commit | !add features ("while I'm here")

## Pressure Resistance
1. "Even if faster" → !skip investigation
2. "Even if urgent" → reproduce before fix
3. "Even if obvious" → evidence confirms
4. "Even if senior says so" → authority ≠ evidence

Investment: 10-30 min investigation → saves hours of symptom-whacking
