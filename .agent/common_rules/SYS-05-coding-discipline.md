---
description: Coding Discipline — Root-Cause Tracing, Blast Radius Analysis, Read-Before-Write (DRY), No Hallucination
tag: "@AI-ONLY"
---

# Coding Discipline

## §1 Root-Cause Tracing (Debugging)
On error logs / bug reports → !propose_fix_immediately

1. **Analyze:** error message, stack trace, related files
2. **5 Whys:** drill from surface symptoms → root logic
3. **Hypothesis:** "Root cause is [X] because [Y]"
4. **Verify first:** propose log/debug/check to prove hypothesis → then write fix

## §2 Blast Radius Analysis
Before modifying method || class || interface || DB schema:

1. **findDeps:** grepFor(all files calling/depending on target component)
2. **listRisks:** enumerate side-effects in other modules
3. **syncPlan:** propose accompanying changes to prevent breakage

## §3 Read-Before-Write (DRY)
- !create_blindly — before new Helper || Service || Component → grepFor(existing similar first)
- inherit architecture: analyze 1-2 similar files → replicate style, error handling, dir structure
- report: "Found similar pattern in [file X]. Applying this pattern."

## §4 No Hallucination (Explicit Uncertainty)
- facts only: code from official docs || existing workspace code — !fabricate(APIs || props || methods)
- if !certain(library || ENV var) → askUser("Need info about [X] version [Y]")
- uncertainty syntax: "I need more information about [library X] version [Y] to complete this task."
