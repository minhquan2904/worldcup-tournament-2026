---
name: learn-thirdparty-call
description: Learn third-party API call patterns — HttpService, retry, error handling, token patterns
tag: "@AI-ONLY"
allowed-tools: [Read, Write, Grep, Glob]
context: fork
version: 3.0
---

# Learn Third-Party Calls (Optional)

> Output: `knowledge_thirdparty.md` → PROPOSE_DIR
> Only run when project has significant external API integrations.

## §1 HTTP Client Infrastructure
- find IHttpService + HttpService → methods (PostAsync, GetAsync), retry, error handling, auth token
- find external API configs → base URLs, timeout, environment settings

## §2 External Service Callers
- scan HttpService/IHttpService/PostAsync/GetAsync in modules/ → per caller: service, endpoint, DTOs, error handling
- scan Infrastructure/3rds/ → RedisService, S3Service, MapperService, other wrappers

## §3 Write Output — Structured NL Format
Output format: **Structured NL** (@AI-ONLY, pipeline context)
- Tables for structured data (class hierarchy, naming, DI mappings)
- Code blocks: keep 100% unchanged (real samples, templates)
- !verbose prose | bullets + shorthand | use cos_convention.md operators
- ALL class names = REAL from source — !placeholders

## Guardrails
- !assume Java patterns (Feign, RestTemplate)
- scan for .NET HttpClient/HttpService
- xref: architecture (3rds overview), service, error_debug
