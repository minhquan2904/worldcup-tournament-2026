# Methodology: Secure Coding & Error Handling (V15, V16)

> Hướng dẫn kiểm tra **V15 (Secure Coding and Architecture)** và **V16 (Security Logging and Error Handling)**.
> File này chứa **HOW to check**. Danh sách rules cụ thể đến từ `owasp_checklist.md`.

---

## Scan Targets

### .NET Backend

| File Pattern | Mục đích kiểm tra |
|---|---|
| `*.csproj` | Third-party package references, versions |
| `*Controller.cs` | Response data exposure, mass assignment |
| `*Service.cs` | Error handling, external URL calls |
| `Startup.cs`, `Program.cs` | Global error handler, exception middleware |
| `*Middleware.cs` | Error handling middleware |
| `*Exception*.cs` | Custom exception classes |
| `*DTO.cs`, `*Request.cs`, `*Response.cs` | Mass assignment protection |

### Angular Frontend

| File Pattern | Mục đích kiểm tra |
|---|---|
| `package.json` | NPM dependencies, known vulnerabilities |
| `*.interceptor.ts` | Error interceptor, global error handling |
| `*.service.ts` | Error handling in HTTP calls |
| `*.component.ts` | Error display, user-facing messages |

---

## V15.1 — Secure Coding Documentation

### Third-party Library Scan

```bash
# .NET — Package references
grep -rn "PackageReference\|Include=\"\|Version=\"" --include="*.csproj"

# Check for known vulnerable packages
# Agent should cross-reference package names with known CVE databases

# Angular — NPM packages
# Read package.json and check for known vulnerabilities
# npm audit (if available)
```

### ✅ Verification Method
```bash
# .NET — List all NuGet packages
grep -rn "<PackageReference" --include="*.csproj" | sort

# Angular — Check outdated/vulnerable
# npm audit --json (output shows vulnerabilities)
```

---

## V15.2 — Security Architecture and Dependencies

### Availability Protection

```bash
# .NET — Rate limiting, timeout, resource limits
grep -rn "RateLimiting\|RateLimit\|Throttle\|ConcurrencyLimiter" --include="*.cs"
grep -rn "Timeout\|CancellationToken\|TaskCanceledException" --include="*.cs"
grep -rn "MaxDegreeOfParallelism\|SemaphoreSlim\|ThrottleAsync" --include="*.cs"
```

### Production Environment

```bash
# .NET — Debug/test code in production
grep -rn "TODO\|HACK\|FIXME\|TEMP\|REMOVE" --include="*.cs"
grep -rn "Console.WriteLine\|Debug.WriteLine\|Debugger.Break" --include="*.cs"
grep -rn "swagger\|Swagger\|UseSwagger\|UseSwaggerUI" --include="*.cs"
```

### ✅ GOOD (.NET)
```csharp
// Only enable Swagger in development
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
```

### ❌ BAD (.NET)
```csharp
// Swagger exposed in all environments
app.UseSwagger();
app.UseSwaggerUI();
```

---

## V15.3 — Defensive Coding

### Mass Assignment Prevention

```bash
# .NET — Bind attribute, DTO vs Entity
grep -rn "\[Bind(\|\[FromBody\]\|AutoMapper\|MapFrom\|CreateMap" --include="*.cs"

# Check if controllers bind directly to entities (BAD)
grep -rn "public.*IActionResult.*Entity\b" --include="*Controller.cs"

# Check for specific DTO Request classes (GOOD)
grep -rn "public.*IActionResult.*Request\b" --include="*Controller.cs"
```

### ✅ GOOD (.NET)
```csharp
// Use specific DTOs — only allowed fields can be set
[HttpPost]
public async Task<IActionResult> Create([FromBody] CreateUserRequest request)
{
    // request only has fields that user is allowed to set
    var entity = _mapper.Map<UserEntity>(request);
    // ...
}
```

### ❌ BAD (.NET)
```csharp
// Binding directly to entity — mass assignment vulnerability
[HttpPost]
public async Task<IActionResult> Create([FromBody] UserEntity entity)
{
    // Attacker can set Role, IsAdmin, etc.
    await _context.Users.AddAsync(entity);
    // ...
}
```

### Data Subset Return

```bash
# .NET — Full entity exposure
grep -rn "return Ok(entity\|return Ok(_context\|\.ToList()" --include="*Controller.cs"

# Proper: return DTO/projection
grep -rn "return Ok(.*Response\|\.Select(\|\.ProjectTo" --include="*Controller.cs"
```

### External URL Redirect Prevention

```bash
# .NET — HTTP client redirect
grep -rn "AllowAutoRedirect\|HttpClientHandler\|MaxAutomaticRedirections" --include="*.cs"
grep -rn "HttpClient\|GetAsync\|PostAsync\|SendAsync" --include="*.cs"
```

### ✅ GOOD (.NET)
```csharp
var handler = new HttpClientHandler
{
    AllowAutoRedirect = false // Don't follow redirects by default
};
var client = new HttpClient(handler);
```

### Type Safety

```bash
# .NET — Weak typing patterns
grep -rn "dynamic\s\|var\s.*=.*\(object\)\|Convert.ChangeType\|as\s" --include="*.cs"
grep -rn "object\s\w+\s*=" --include="*.cs"
```

---

## V16 — Security Logging and Error Handling

### V16.5 — Error Handling

```bash
# .NET — Global exception handler
grep -rn "UseExceptionHandler\|ExceptionHandlerMiddleware\|IExceptionHandler" --include="*.cs"
grep -rn "ExceptionFilter\|OnException\|HandleException" --include="*.cs"

# Stack trace exposure
grep -rn "ex.StackTrace\|ex.Message\|ex.ToString()\|Exception.*response\|InnerException" --include="*.cs"
grep -rn "UseDeveloperExceptionPage" --include="*.cs"

# Generic error message
grep -rn "500.*error\|Internal Server Error\|Something went wrong\|Đã xảy ra lỗi" --include="*.cs"
```

### ✅ GOOD (.NET)
```csharp
// Global exception handler — returns generic message
app.UseExceptionHandler(errorApp =>
{
    errorApp.Run(async context =>
    {
        context.Response.StatusCode = 500;
        context.Response.ContentType = "application/json";
        await context.Response.WriteAsJsonAsync(new
        {
            Status = 500,
            Message = "An unexpected error occurred. Please try again later."
        });

        // Log the real exception internally
        var exception = context.Features.Get<IExceptionHandlerFeature>()?.Error;
        _logger.LogError(exception, "Unhandled exception");
    });
});
```

### ❌ BAD (.NET)
```csharp
// Exposing exception details to client
catch (Exception ex)
{
    return BadRequest(new
    {
        Error = ex.Message,
        StackTrace = ex.StackTrace,
        InnerException = ex.InnerException?.Message
    });
}
```

### Circuit Breaker / Graceful Degradation

```bash
# .NET — Resilience patterns
grep -rn "Polly\|CircuitBreaker\|RetryPolicy\|FallbackPolicy\|BulkheadPolicy" --include="*.cs"
grep -rn "AddResilienceHandler\|AddStandardResilienceHandler" --include="*.cs"

# Try-catch in external calls
grep -rn "try\s*{\s*\n.*HttpClient\|try\s*{\s*\n.*GetAsync\|try\s*{\s*\n.*SendAsync" --include="*.cs"
```

### Fail-Safe Patterns

```bash
# .NET — Transaction handling on error
grep -rn "TransactionScope\|BeginTransaction\|CommitAsync\|RollbackAsync" --include="*.cs"
grep -rn "catch.*Rollback\|catch.*transaction" --include="*.cs"

# Check for fail-open conditions
grep -rn "catch.*continue\|catch.*return Ok\|catch.*return true" --include="*.cs"
```

### ✅ GOOD (.NET)
```csharp
// Fail-safe: rollback on error
using var transaction = await _context.Database.BeginTransactionAsync();
try
{
    await _service.ProcessPayment(request);
    await transaction.CommitAsync();
}
catch (Exception ex)
{
    await transaction.RollbackAsync();
    _logger.LogError(ex, "Payment processing failed");
    throw; // Re-throw to global handler
}
```

### ❌ BAD (.NET)
```csharp
// Fail-open: continues processing despite validation error
try
{
    ValidateTransaction(request);
}
catch (Exception)
{
    // Swallowed exception — transaction continues without validation
}
await ProcessTransaction(request);
```
