# Methodology: Web Frontend & API Security (V3, V4)

> Hướng dẫn cách kiểm tra các OWASP rules thuộc **V3 (Web Frontend Security)** và **V4 (API and Web Service)**.
> File này chứa **HOW to check**. Danh sách rules cụ thể đến từ `owasp_checklist.md`.

---

## Scan Targets

### .NET Backend

| File Pattern | Mục đích kiểm tra |
|---|---|
| `Startup.cs`, `Program.cs` | CORS, HSTS, CSP, middleware pipeline |
| `*Controller.cs` | HTTP methods, Content-Type, response headers |
| `appsettings*.json` | CORS allowed origins, HTTPS redirect settings |
| `*Middleware.cs` | Custom header injection, security headers |

### Angular Frontend

| File Pattern | Mục đích kiểm tra |
|---|---|
| `index.html` | CSP meta tags, HSTS |
| `*.interceptor.ts` | Custom headers, token handling |
| `*.guard.ts` | Route protection |
| `*.component.ts/html` | Content rendering, text vs HTML |
| `angular.json` | Build settings, CSP nonce |

---

## V3.2 — Unintended Content Interpretation

```bash
# Angular — Unsafe rendering
grep -rn "innerHTML\|outerHTML\|\[innerHTML\]" --include="*.html" --include="*.ts"
grep -rn "bypassSecurityTrust" --include="*.ts"

# .NET — Content-Type in responses
grep -rn "ContentType\|MediaTypeHeaderValue\|Produces(" --include="*.cs"
```

### ✅ GOOD (Angular)
```html
<!-- Use textContent for user data -->
<span [textContent]="userData"></span>
```

### ❌ BAD (Angular)
```html
<!-- Never bind untrusted HTML directly -->
<div [innerHTML]="userInput"></div>
```

---

## V3.4 — Browser Security Mechanism Headers

### HSTS

```bash
# .NET — HSTS configuration
grep -rn "UseHsts\|HstsOptions\|Strict-Transport-Security\|MaxAge" --include="*.cs"
grep -rn "app.UseHttpsRedirection" --include="*.cs"
```

### ✅ GOOD (.NET)
```csharp
services.AddHsts(options =>
{
    options.MaxAge = TimeSpan.FromDays(365);
    options.IncludeSubDomains = true;
    options.Preload = true;
});
app.UseHsts();
app.UseHttpsRedirection();
```

### CORS

```bash
# .NET — CORS configuration
grep -rn "AddCors\|UseCors\|WithOrigins\|AllowAnyOrigin\|AllowAnyMethod\|AllowAnyHeader" --include="*.cs"
grep -rn "Access-Control-Allow-Origin" --include="*.cs"
```

### ✅ GOOD (.NET)
```csharp
services.AddCors(options =>
{
    options.AddPolicy("Production", builder =>
        builder.WithOrigins("https://app.example.com")
               .WithMethods("GET", "POST", "PUT", "DELETE")
               .WithHeaders("Authorization", "Content-Type"));
});
```

### ❌ BAD (.NET)
```csharp
// AllowAnyOrigin = open to CSRF/data theft
builder.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader();
```

### CSP (Content Security Policy)

```bash
# .NET — CSP header
grep -rn "Content-Security-Policy\|ContentSecurityPolicy\|frame-ancestors\|script-src\|default-src" --include="*.cs"
grep -rn "X-Content-Type-Options\|nosniff" --include="*.cs"
grep -rn "X-Frame-Options\|DENY\|SAMEORIGIN" --include="*.cs"

# Angular — CSP meta tag
grep -rn "Content-Security-Policy\|http-equiv" --include="index.html"
```

---

## V3.5 — Browser Origin Separation

```bash
# .NET — Check HTTP method restrictions
grep -rn "\[HttpGet\]\|\[HttpPost\]\|\[HttpPut\]\|\[HttpDelete\]\|\[HttpPatch\]" --include="*.cs"

# Check for methods without explicit HTTP method attribute
grep -rn "public.*IActionResult\|public.*async.*Task<" --include="*Controller.cs"

# Angular — Check for GET requests mutating data
grep -rn "this.http.get.*delete\|this.http.get.*update\|this.http.get.*create" --include="*.service.ts"
```

---

## V4.1 — Generic Web Service Security

```bash
# .NET — Content-Type validation
grep -rn "\[Consumes(\|\[Produces(" --include="*.cs"

# HTTP to HTTPS redirect
grep -rn "UseHttpsRedirection\|RequireHttpsAttribute\|HttpsOnly" --include="*.cs"

# Header override protection
grep -rn "X-Forwarded-For\|X-Real-IP\|ForwardedHeaders" --include="*.cs"
```

---

## V4.2 — HTTP Message Structure Validation

```bash
# .NET — Request size limits
grep -rn "RequestSizeLimit\|MaxRequestBodySize\|RequestBodySizeLimit" --include="*.cs"

# Header injection prevention
grep -rn "\\\\r\\\\n\|\\r\\n\|CRLF" --include="*.cs"
```

---

## V4.3 — GraphQL

```bash
# .NET — GraphQL configuration
grep -rn "GraphQL\|HotChocolate\|GraphQLServer" --include="*.cs"
grep -rn "MaxDepth\|MaxComplexity\|IntrospectionAllowed\|EnableIntrospection" --include="*.cs"
```

---

## V4.4 — WebSocket

```bash
# .NET — WebSocket configuration
grep -rn "UseWebSockets\|WebSocketMiddleware\|WebSocket" --include="*.cs"
grep -rn "wss://\|ws://" --include="*.cs" --include="*.ts"

# Angular — WebSocket usage
grep -rn "WebSocket\|webSocket(\|socket.io" --include="*.ts"
```

### ✅ GOOD
```csharp
// Validate WebSocket Origin
app.UseWebSockets(new WebSocketOptions
{
    AllowedOrigins = { "https://app.example.com" }
});
```

### ❌ BAD
```csharp
// No origin validation — open to cross-site WebSocket hijacking
app.UseWebSockets();
```
