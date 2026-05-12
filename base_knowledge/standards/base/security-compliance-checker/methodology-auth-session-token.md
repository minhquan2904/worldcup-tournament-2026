# Methodology: Authentication, Session, Authorization & Tokens (V6, V7, V8, V9)

> Hướng dẫn cách kiểm tra các OWASP rules thuộc **V6 (Authentication)**, **V7 (Session Management)**, **V8 (Authorization)**, **V9 (Tokens)**.
> File này chứa **HOW to check**. Danh sách rules cụ thể đến từ `owasp_checklist.md`.

---

## Scan Targets

### .NET Backend

| File Pattern | Mục đích kiểm tra |
|---|---|
| `Startup.cs`, `Program.cs` | Auth middleware, session config, JWT config |
| `*Controller.cs` | `[Authorize]`, role checks, RBAC |
| `*Service.cs` | Auth logic, password hashing, token generation |
| `appsettings*.json` | Session timeout, JWT secret, cookie config |
| `*Middleware.cs` | Auth middleware, token validation |
| `*Handler.cs` | Custom auth handlers |
| `*IdentityConfig*` | Identity framework configuration |

### Angular Frontend

| File Pattern | Mục đích kiểm tra |
|---|---|
| `*.guard.ts` | Auth guards, route protection |
| `*.interceptor.ts` | Token attachment, refresh logic |
| `auth*.service.ts`, `login*.ts` | Login flow, token storage |
| `*.component.ts` | Logout functionality, session handling |
| `environment*.ts` | Token config, API endpoints |

---

## V6 — Authentication

### V6.2 — Password Security

```bash
# .NET — Password policy configuration
grep -rn "PasswordOptions\|RequiredLength\|RequireDigit\|RequireUppercase\|RequireNonAlphanumeric" --include="*.cs"
grep -rn "PasswordHasher\|BCrypt\|Argon2\|PBKDF2\|HashPassword" --include="*.cs"
grep -rn "MinimumLength\|MaximumLength\|Password" --include="*.cs"

# Angular — Password input type
grep -rn "type=\"password\"\|type='password'" --include="*.html"
grep -rn "password.*text\|type.*text.*password" --include="*.html"
```

### ✅ GOOD (.NET)
```csharp
services.Configure<IdentityOptions>(options =>
{
    options.Password.RequiredLength = 8; // minimum 8, recommended 15
    options.Password.RequireDigit = true;
    options.Password.RequireUppercase = true;
    options.Password.RequireNonAlphanumeric = true;
});
```

### ❌ BAD (.NET)
```csharp
// Weak password policy
options.Password.RequiredLength = 4;
options.Password.RequireDigit = false;
```

### V6.3 — General Authentication

```bash
# .NET — Default accounts
grep -rn "\"admin\"\|\"root\"\|\"sa\"\|\"test\"\|\"demo\"" --include="*.cs" --include="appsettings*.json"
grep -rn "DefaultPassword\|DefaultUser\|SeedData" --include="*.cs"
```

### V6.4 — Authentication Factor Lifecycle

```bash
# .NET — Password reset flow
grep -rn "ResetPassword\|ForgotPassword\|ChangePassword\|GeneratePasswordReset" --include="*.cs"

# BO-specific: Admin password reset
grep -rn "AdminResetPassword\|ForceResetPassword\|SetPassword" --include="*.cs"
```

---

## V7 — Session Management

### V7.1 — Session Documentation & Config

```bash
# .NET — Session configuration
grep -rn "AddSession\|UseSession\|SessionOptions\|IdleTimeout\|Cookie.MaxAge\|ExpireTimeSpan" --include="*.cs"
grep -rn "SessionTimeout\|session.*timeout\|idle.*timeout" --include="appsettings*.json"

# Concurrent sessions
grep -rn "MaxConcurrentSessions\|ActiveSessions\|SessionCount\|KickUser" --include="*.cs"
```

### V7.2 — Fundamental Session Security

```bash
# .NET — Token generation
grep -rn "GenerateToken\|RefreshToken\|CreateToken\|JwtSecurityToken\|SecurityTokenDescriptor" --include="*.cs"

# Static API keys — BAD
grep -rn "ApiKey\|api_key\|x-api-key\|hardcoded.*key\|static.*secret" --include="*.cs" --include="appsettings*.json"

# Angular — Session token in storage
grep -rn "localStorage\|sessionStorage\|IndexedDB" --include="*.ts"
grep -rn "setItem.*token\|getItem.*token" --include="*.ts"
```

### V7.3 — Session Timeout

```bash
# .NET — Inactivity timeout
grep -rn "SlidingExpiration\|AbsoluteExpiration\|IdleTimeout\|ExpireTimeSpan" --include="*.cs"

# Angular — Auto logout timer
grep -rn "setTimeout.*logout\|idle.*timeout\|session.*expire" --include="*.ts"
```

### V7.4 — Session Termination

```bash
# .NET — Logout and session kill
grep -rn "SignOut\|Logout\|RemoveToken\|RevokeToken\|InvalidateSession\|ClearSession" --include="*.cs"

# Kill all sessions on password change
grep -rn "RevokeAllTokens\|InvalidateAllSessions\|KickAllUsers\|TerminateActiveSessions" --include="*.cs"

# Angular — Logout UI
grep -rn "logout\|signOut\|sign-out" --include="*.html" --include="*.ts"
```

### ✅ GOOD (.NET)
```csharp
public async Task<IActionResult> Logout()
{
    await _tokenService.RevokeAllUserTokens(userId);
    await HttpContext.SignOutAsync();
    return Ok();
}
```

### ❌ BAD (.NET)
```csharp
// Only clears cookie, doesn't invalidate server-side token
public IActionResult Logout()
{
    Response.Cookies.Delete("auth_token");
    return Ok();
}
```

---

## V8 — Authorization

### V8.1–V8.2 — Authorization Design

```bash
# .NET — Authorize attribute
grep -rn "\[Authorize\]\|\[Authorize(\|\[AllowAnonymous\]" --include="*.cs"
grep -rn "Policy\s*=\|Roles\s*=\|RequireClaim\|RequireRole" --include="*.cs"

# Missing authorization — controllers without [Authorize]
grep -rn "public class.*Controller" --include="*Controller.cs"

# IDOR prevention — check if user ID is validated
grep -rn "userId\|currentUser\|User.Identity\|User.Claims" --include="*.cs"
```

### V8.3 — Operation Level Authorization

```bash
# .NET — Server-side authorization enforcement
grep -rn "IAuthorizationService\|AuthorizeAsync\|AuthorizationHandler" --include="*.cs"

# Angular — Client-side only auth (BAD if no server enforcement)
grep -rn "canActivate\|canDeactivate\|isAdmin\|hasPermission\|hasPrivilege" --include="*.ts"
```

### ✅ GOOD (.NET)
```csharp
[Authorize(Policy = "RequireAdminRole")]
[HttpDelete("{id}")]
public async Task<IActionResult> Delete(int id)
{
    // Verify ownership before deleting
    var entity = await _service.GetById(id);
    if (entity.CreatedBy != CurrentUserId && !User.IsInRole("Admin"))
        return Forbid();
    // ...
}
```

### ❌ BAD (.NET)
```csharp
// No authorization — any authenticated user can delete anything
[HttpDelete("{id}")]
public async Task<IActionResult> Delete(int id)
{
    await _service.Delete(id);
    return Ok();
}
```

---

## V9 — Self-contained Tokens

### V9.1 — Token Integrity

```bash
# .NET — JWT configuration
grep -rn "JwtBearerDefaults\|AddJwtBearer\|TokenValidationParameters" --include="*.cs"
grep -rn "ValidateIssuerSigningKey\|IssuerSigningKey\|ValidateIssuer\|ValidateAudience\|ValidateLifetime" --include="*.cs"

# JWT secret in settings
grep -rn "SecretKey\|JwtSecret\|SigningKey\|SymmetricSecurityKey" --include="*.cs" --include="appsettings*.json"

# Dangerous: algorithm none or weak
grep -rn "SecurityAlgorithms.None\|alg.*none\|HmacSha256\b" --include="*.cs"
```

### V9.2 — Token Content

```bash
# .NET — Token expiration
grep -rn "Expires\|NotBefore\|ValidTo\|ClockSkew\|TokenLifetime" --include="*.cs"

# Token type validation
grep -rn "access_token\|refresh_token\|token_type\|Bearer" --include="*.cs"
```

### ✅ GOOD (.NET)
```csharp
var tokenValidationParameters = new TokenValidationParameters
{
    ValidateIssuerSigningKey = true,
    IssuerSigningKey = new SymmetricSecurityKey(key),
    ValidateIssuer = true,
    ValidateAudience = true,
    ValidateLifetime = true,
    ClockSkew = TimeSpan.Zero
};
```

### ❌ BAD (.NET)
```csharp
// Disabling signature validation — critically vulnerable
var parameters = new TokenValidationParameters
{
    ValidateIssuerSigningKey = false,
    ValidateIssuer = false,
    ValidateAudience = false,
    ValidateLifetime = false
};
```
