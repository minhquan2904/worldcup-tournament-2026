# Methodology: Injection & Sanitization (V1)

> Hướng dẫn cách kiểm tra các OWASP rules thuộc **Chapter V1 — Encoding and Sanitization**.
> File này chứa **HOW to check**. Danh sách rules cụ thể đến từ `owasp_checklist.md`.

---

## Scan Targets

### .NET Backend

| File Pattern | Mục đích kiểm tra |
|---|---|
| `*Service.cs` | Input handling, data processing logic |
| `*Controller.cs` | Request binding, parameter handling |
| `*Repository.cs` | Database queries |
| `*Helper.cs`, `*Util*.cs` | Utility functions dealing with string/data |
| `Startup.cs`, `Program.cs` | Middleware configuration, XML parser config |
| `appsettings*.json` | Configuration values |

### Angular Frontend

| File Pattern | Mục đích kiểm tra |
|---|---|
| `*.component.ts` | DOM manipulation, innerHTML usage |
| `*.component.html` | Template bindings, unsafe interpolation |
| `*.service.ts` | HTTP calls, URL construction |
| `*.pipe.ts` | Data transformation |

---

## V1.1 — Encoding and Sanitization Architecture

### Grep Patterns

```bash
# .NET — Check for multiple decode/unescape calls
grep -rn "HttpUtility.UrlDecode\|WebUtility.UrlDecode\|Uri.UnescapeDataString\|HtmlDecode" --include="*.cs"

# Angular — Check for decodeURIComponent chains
grep -rn "decodeURIComponent\|decodeURI\|unescape(" --include="*.ts"
```

### ✅ GOOD (.NET)
```csharp
// Decode once, then validate
var decoded = Uri.UnescapeDataString(input);
var sanitized = InputValidator.Sanitize(decoded);
```

### ❌ BAD (.NET)
```csharp
// Double decode — bypass vulnerability
var decoded = Uri.UnescapeDataString(Uri.UnescapeDataString(input));
```

---

## V1.2 — Injection Prevention

### SQL Injection

```bash
# .NET — Dangerous: string concatenation in queries
grep -rn "string.Format.*SELECT\|\"SELECT.*\" +\|$\"SELECT.*{" --include="*.cs"
grep -rn "ExecuteSqlRaw\|FromSqlRaw" --include="*.cs"

# Safe: parameterized queries
grep -rn "SqlParameter\|AddWithValue\|FromSqlInterpolated" --include="*.cs"
```

### ✅ GOOD (.NET)
```csharp
var result = await context.Users
    .FromSqlInterpolated($"SELECT * FROM Users WHERE Id = {userId}")
    .ToListAsync();
```

### ❌ BAD (.NET)
```csharp
var sql = $"SELECT * FROM Users WHERE Name = '{userName}'";
var result = context.Database.ExecuteSqlRaw(sql);
```

### URL Building

```bash
# .NET — Dynamic URL construction
grep -rn "string.Format.*http\|$\"http.*{" --include="*.cs"
grep -rn "Redirect(\|RedirectToAction(" --include="*.cs"

# Angular — Dynamic URL construction
grep -rn "window.location\|document.location\|window.open(" --include="*.ts"
grep -rn "this.router.navigate\|this.router.navigateByUrl" --include="*.ts"
```

### OS Command Injection

```bash
# .NET — Process execution
grep -rn "Process.Start\|ProcessStartInfo\|System.Diagnostics.Process" --include="*.cs"
grep -rn "cmd.exe\|/bin/bash\|powershell" --include="*.cs"
```

### LDAP Injection (PIC=BO specific)

```bash
# .NET — LDAP queries
grep -rn "DirectorySearcher\|DirectoryEntry\|SearchFilter\|LdapConnection" --include="*.cs"
grep -rn "(&(objectClass=" --include="*.cs"
```

### XPath Injection

```bash
# .NET — XPath queries
grep -rn "XPathNavigator\|SelectNodes\|SelectSingleNode\|XmlDocument.Select" --include="*.cs"
```

### Dynamic Code Execution

```bash
# .NET — Dangerous eval-like patterns
grep -rn "CSharpScript.Evaluate\|Roslyn\|CodeDom\|Reflection.Emit\|DynamicMethod\|Assembly.Load" --include="*.cs"

# Angular — eval and similar
grep -rn "eval(\|Function(\|setTimeout.*string\|setInterval.*string" --include="*.ts"
grep -rn "innerHTML\|outerHTML\|document.write" --include="*.ts" --include="*.html"
```

### ✅ GOOD (Angular)
```typescript
// Use Angular's built-in sanitization
this.sanitizer.bypassSecurityTrustHtml(content); // Only when content is trusted
// Better: use [textContent] instead of [innerHTML]
```

### ❌ BAD (Angular)
```typescript
// Direct eval — NEVER DO THIS
eval(userInput);
// Unsafe innerHTML with user data
element.innerHTML = userProvidedHtml;
```

---

## V1.3 — Sanitization

### HTML Sanitization

```bash
# .NET — HTML sanitization libraries
grep -rn "HtmlSanitizer\|AngleSharp\|Ganss.Xss" --include="*.cs"
grep -rn "AllowedTags\|AllowedAttributes\|SanitizeHtml" --include="*.cs"

# Angular — Bypass security
grep -rn "bypassSecurityTrustHtml\|bypassSecurityTrustScript\|bypassSecurityTrustUrl\|bypassSecurityTrustResourceUrl\|bypassSecurityTrustStyle" --include="*.ts"
```

### Template Injection (SSTI)

```bash
# .NET — Template engines
grep -rn "RazorEngine\|Scriban\|Liquid\|Handlebars\|Mustache" --include="*.cs"
grep -rn "Template.Parse\|template.Render" --include="*.cs"
```

### CSV/Formula Injection

```bash
# .NET — CSV export
grep -rn "StreamWriter\|CsvWriter\|StringBuilder.*csv\|text/csv\|application/csv" --include="*.cs"
grep -rn "=\"\|=HYPERLINK\|=CMD\|=SUM\|+CMD" --include="*.cs"
```

---

## V1.4 — Memory, String, and Unmanaged Code

```bash
# .NET — Unsafe code and unmanaged resources
grep -rn "unsafe\s*{" --include="*.cs"
grep -rn "Marshal\.\|IntPtr\|GCHandle\|stackalloc\|fixed\s*(" --include="*.cs"
grep -rn "IDisposable\|using\s*(" --include="*.cs"
```

---

## V1.5 — Safe Deserialization

```bash
# .NET — Dangerous deserialization
grep -rn "BinaryFormatter\|SoapFormatter\|NetDataContractSerializer\|ObjectStateFormatter" --include="*.cs"
grep -rn "JsonConvert.DeserializeObject\|JsonSerializer.Deserialize" --include="*.cs"
grep -rn "XmlSerializer\|DataContractSerializer" --include="*.cs"

# XML parser config — check for XXE protection
grep -rn "XmlReaderSettings\|DtdProcessing\|ProhibitDtd\|XmlResolver" --include="*.cs"

# Angular — JSON parsing
grep -rn "JSON.parse(" --include="*.ts"
```

### ✅ GOOD (.NET)
```csharp
var settings = new XmlReaderSettings
{
    DtdProcessing = DtdProcessing.Prohibit,
    XmlResolver = null
};
```

### ❌ BAD (.NET)
```csharp
// BinaryFormatter is inherently unsafe — NEVER use
var formatter = new BinaryFormatter();
var obj = formatter.Deserialize(stream);
```
