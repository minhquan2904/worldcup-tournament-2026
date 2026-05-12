# Proposal: <!-- feature-name -->

> **Type**: NEWBUILD|MAINTENANCE | **Module**: <!-- module --> | **Schema**: <!-- db_schema -->

## Why
<!-- 2-3 lines: business motivation, what problem, why now -->

## What Changes
<!-- numbered list: 1-line per change (Entity, API, Service, Controller, DTO) -->

## Capabilities

### New
<!-- - `capability-name`: one-line description -->

### Modified
<!-- - `capability-name`: what requirement changed (or "None") -->

## Impact
<!-- - DB: schema, tables, backward compat -->
<!-- - API: endpoints, backward compat -->
<!-- - Deps: existing services used -->
<!-- - Auth: FunctionConst range -->

## Feature Profile
```
Mode: CRUD|REPORT | Entity: BaseFieldEntity|... | Service: IScoped|...
Controller: BaseController | Type: NEWBUILD|MAINTENANCE | Approval: Yes|No
DbContext: <!-- existing/new -->
```
