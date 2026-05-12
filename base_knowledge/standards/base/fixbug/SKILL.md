---
name: fixbug
when_to_use: Systematic bug diagnosis — hypothesis-driven RCA, minimal fix, regression prevention.
paths: [base_knowledge/standards/base/fixbug/]
---

# Fixbug — Systematic Bug Diagnosis & Fix

> NEVER fix symptoms. ALWAYS find root cause.
> Tech-specific debug patterns → project-level standards/fixbug/ (dotnet-debug-patterns.md, angular-debug-patterns.md, cross-layer-debug.md)

## Sub-Files
| File | When |
|------|------|
| systematic-debugging.md | BẮT BUỘC — 4-phase investigation framework |
| root-cause-tracing.md | Bug sâu trong call stack |
| defense-in-depth.md | Post-fix hardening (4-layer validation) |

## Core Principles
- Root cause ONLY — fix at origin, !at error point
- Single hypothesis — test ONE at a time, !shotgun debugging
- Minimal fix — smallest change, !refactor alongside
- Evidence-backed — log, stack trace, reproduction
- Regression prevention — every fix MUST have test

## 6-Phase Methodology
1. **Reproduce** 🔴 — reproduce 100% reliable BEFORE fixing. ⛔ !proceed without
2. **Isolate** 🔍 — narrow scope (layer/file/function), trace backward, check git log
3. **Hypothesize** 🧠 — list 2-5 causes, rank (Occam's Razor), test prediction. ⛔ Rejected? → back to Phase 2
4. **Fix** 🟢 — write failing test (RED), implement smallest fix (GREEN), !refactor
5. **Verify** ✅ — reproduction steps pass, edge cases tested, no regression, builds
6. **Harden** 🛡️ — defense-in-depth, check similar patterns, document root cause

## Anti-Patterns
❌ Fix without reproduce | ❌ Shotgun debugging (multiple changes) | ❌ Fix symptoms
❌ Skip test "too small" | ❌ Refactor in fix commit | ❌ sleep()/delay() for timing bugs
❌ Fix #2 on top of failed fix #1 → STOP, re-hypothesize
