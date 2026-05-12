# Root Cause Tracing — Backward Call-Chain Analysis

> Fix at source, !at error point. Trace backward through call chain.

## When to Use
✅ Error deep in call stack (>5 levels) | ✅ Unknown data origin
❌ Clear entry point error (fix directly)

## 5-Step Process
1. **Observe Symptom** — full error message + context + line number
2. **Find Immediate Cause** — code directly causing error (entity=null, response.data=undefined)
3. **Ask: What Called This?** — trace backward 1 level (Controller→Service→Repository)
4. **Keep Tracing Up** — ask "where did wrong data come from?" until source found
5. **Fix at Source** — !null check at symptom point → fix route/DTO/config at origin

## Stack Trace Reading
### .NET
- Read bottom→up. Bottom=entry point, top=crash point
- Skip System.*, Microsoft.* frames → focus on OUR code (BOModule.*)
- Each frame = 1 level to trace

### Angular
- Focus on .component.ts, .service.ts, .module.ts files
- Skip core.mjs, router.mjs frames
- Check line number → open file at that line

## Debug Instrumentation (temporary)
- .NET: _logger.LogWarning("DEBUG: id={Id}, caller={Caller}", id, stackTrace)
- Angular: console.warn('DEBUG', { timestamp, route, params })
- ⚠️ DELETE debug logging after fix. !commit debug logs.

## Key Principle
```
Found immediate cause → Can trace up? 
  YES → Trace backward → Is this source? 
    YES → Fix at source + validate each layer → Bug impossible ✅
    NO → Keep tracing
  NO → Fix at deepest point
```
