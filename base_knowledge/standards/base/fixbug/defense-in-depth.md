# Defense-in-Depth — Multi-Layer Validation After Fix

> Single check can be bypassed. Validate at EVERY layer. Make bug structurally impossible.

## Four Layers
1. **Entry Point** — reject obviously invalid input at API/component boundary
   - C#: guard clause in Controller (id <= 0 → BadRequest)
   - Angular: route param validation → redirect if invalid
2. **Business Logic** — ensure data makes sense for the operation
   - C#: ArgumentException + NotFoundException in Service
   - Angular: Observable throwError for invalid params
3. **Infrastructure Guards** — database/framework level constraints
   - EF Core: .IsRequired(), .HasMaxLength(), .HasIndex().IsUnique()
   - Angular: HTTP interceptor catches unhandled errors
4. **Debug Instrumentation** — LogDebug context for forensics
   - Use LogDebug level → !show in production logs
   - Delete after fix confirmed

## After Fix — Apply Pattern
1. Map data flow → how many layers does data pass through?
2. List checkpoints → each layer = 1 checkpoint
3. Add validation → minimum Layer 1 + Layer 2
4. Test bypass → bypass Layer 1, verify Layer 2 catches

## When to Apply
✅ Invalid data flowing through | ✅ Null/empty values | ⚠️ Type mismatch
❌ Logic error (fix directly) | ❌ Missing feature (implement)
