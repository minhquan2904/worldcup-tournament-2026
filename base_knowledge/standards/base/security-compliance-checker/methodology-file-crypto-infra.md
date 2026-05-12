# Methodology: File Handling, Cryptography & Infrastructure (V5, V11–V14)

> Hướng dẫn kiểm tra **V5 (File Handling)**, **V11 (Cryptography)**, **V12 (Secure Communication)**, **V13 (Configuration)**, **V14 (Data Protection)**.
> File này chứa **HOW to check**. Danh sách rules cụ thể đến từ `owasp_checklist.md`.

---

## Scan Targets

### .NET Backend

| File Pattern | Mục đích kiểm tra |
|---|---|
| `*Controller.cs` | File upload endpoints, download endpoints |
| `*Service.cs` | File processing, virus scanning, TLS calls |
| `Startup.cs`, `Program.cs` | HTTPS config, HSTS, certificate validation |
| `appsettings*.json` | TLS version, certificate paths, file size limits |
| `*Middleware.cs` | Security headers, caching headers |

### Angular Frontend

| File Pattern | Mục đích kiểm tra |
|---|---|
| `*.component.ts/html` | File upload components, download buttons |
| `*.service.ts` | HTTP calls (https vs http) |
| `*.interceptor.ts` | Cache-Control headers |
| `index.html` | Meta tags, cache control |

---

## V5 — File Handling

### V5.1 — File Handling Documentation & V5.2 — Upload

```bash
# .NET — File upload handling
grep -rn "IFormFile\|FromForm\|Upload\|MultipartBody" --include="*.cs"
grep -rn "ContentLength\|MaxRequestBodySize\|RequestSizeLimit\|MaxFileSize" --include="*.cs"

# File type validation
grep -rn "ContentType\|MimeType\|\.Extension\|AllowedExtensions\|AllowedMimeTypes" --include="*.cs"
grep -rn "\.jpg\|\.png\|\.pdf\|\.xlsx\|\.docx" --include="*.cs"

# Image pixel validation
grep -rn "Image.FromStream\|Bitmap\|ImageSharp\|Width\|Height\|MaxWidth\|MaxHeight" --include="*.cs"
```

### ✅ GOOD (.NET)
```csharp
public async Task<IActionResult> Upload(IFormFile file)
{
    // Validate file size
    if (file.Length > _maxFileSize)
        return BadRequest("File too large");

    // Validate extension
    var ext = Path.GetExtension(file.FileName).ToLower();
    if (!_allowedExtensions.Contains(ext))
        return BadRequest("Invalid file type");

    // Validate content type matches extension
    if (!IsValidContentType(file.ContentType, ext))
        return BadRequest("Content type mismatch");

    // Scan for virus
    await _antivirusService.Scan(file.OpenReadStream());
    // ...
}
```

### ❌ BAD (.NET)
```csharp
// No validation — accepts anything
public async Task<IActionResult> Upload(IFormFile file)
{
    var path = Path.Combine(_uploads, file.FileName);
    using var stream = new FileStream(path, FileMode.Create);
    await file.CopyToAsync(stream);
    return Ok();
}
```

### V5.4 — File Download

```bash
# .NET — File download / Content-Disposition
grep -rn "Content-Disposition\|ContentDisposition\|FileResult\|FileStreamResult\|PhysicalFile" --include="*.cs"
grep -rn "FileName\|attachment;\|inline;" --include="*.cs"

# Antivirus scanning
grep -rn "AntiVirus\|VirusScan\|Malware\|ClamAV\|OPSWAT\|MetaDefender" --include="*.cs"
```

---

## V11 — Cryptography

### V11.7 — In-Use Data Cryptography

```bash
# .NET — Data encryption
grep -rn "AES\|Rijndael\|RSA\|DataProtection\|IDataProtector\|Encrypt\|Decrypt" --include="*.cs"
grep -rn "ProtectedData\|SecureString\|CryptographicException" --include="*.cs"

# Weak algorithms
grep -rn "MD5\|SHA1\|DES\|RC2\|RC4\|TripleDES" --include="*.cs"
```

---

## V12 — Secure Communication

### V12.1 — TLS Configuration

```bash
# .NET — TLS settings
grep -rn "SslProtocols\|Tls12\|Tls13\|Tls11\|Ssl3" --include="*.cs"
grep -rn "ServicePointManager\|SecurityProtocol" --include="*.cs"
grep -rn "ServerCertificateCustomValidationCallback" --include="*.cs"

# Certificate validation
grep -rn "RemoteCertificateValidationCallback\|ServerCertificateValidationCallback" --include="*.cs"
grep -rn "return true" --include="*.cs"  # Dangerous if in cert validation callback
```

### ✅ GOOD (.NET)
```csharp
// Force TLS 1.2+
services.AddHttpClient("external")
    .ConfigurePrimaryHttpMessageHandler(() => new HttpClientHandler
    {
        SslProtocols = SslProtocols.Tls12 | SslProtocols.Tls13
    });
```

### ❌ BAD (.NET)
```csharp
// Disabling certificate validation — NEVER DO THIS IN PRODUCTION
ServicePointManager.ServerCertificateValidationCallback =
    (sender, cert, chain, errors) => true;
```

### V12.2–V12.3 — HTTPS & Service-to-Service

```bash
# .NET — HTTP vs HTTPS calls
grep -rn "http://" --include="*.cs" --include="appsettings*.json"
grep -rn "https://" --include="*.cs" --include="appsettings*.json"

# Angular — Insecure HTTP calls
grep -rn "http://" --include="*.ts" --include="environment*.ts"
```

---

## V13 — Configuration

### V13.4 — Information Leakage

```bash
# .NET — Directory browsing
grep -rn "UseDirectoryBrowser\|DirectoryBrowser\|UseStaticFiles" --include="*.cs"

# Debug mode in production
grep -rn "UseDeveloperExceptionPage\|IsDevelopment\|EnableDetailedErrors" --include="*.cs"
```

---

## V14 — Data Protection

### V14.3 — Client-side Data Protection

```bash
# .NET — Cache-Control headers
grep -rn "Cache-Control\|no-store\|no-cache\|Pragma" --include="*.cs"
grep -rn "ResponseCaching\|OutputCache" --include="*.cs"

# Angular — Browser storage with sensitive data
grep -rn "localStorage.setItem\|sessionStorage.setItem" --include="*.ts"
grep -rn "password\|secret\|token\|credit.*card\|ssn\|pin" --include="*.ts"
```

### ✅ GOOD (.NET)
```csharp
// Anti-caching for sensitive responses
app.Use(async (context, next) =>
{
    context.Response.Headers["Cache-Control"] = "no-store, no-cache, must-revalidate";
    context.Response.Headers["Pragma"] = "no-cache";
    await next();
});
```
