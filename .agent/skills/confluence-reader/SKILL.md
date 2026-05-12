---
name: confluence-reader
description: Read Confluence pages recursively — detect hierarchy, discover links, ingest all content.
arguments: ["${page_url_or_id}"]
allowed-tools: [Read, Write, MCP]
context: inline
version: 3.0
---

# Confluence Reader

Output: Structured markdown with all page content (root + children + linked)

## Input
| Param | Required | Default |
|-------|----------|---------|
| CONFLUENCE_URL or PAGE_ID | Yes (1 of 2) | — |
| MAX_DEPTH | No | 3 |
| FOLLOW_LINKS | No | true |

## §1 Parse Input → Page ID
URL patterns: /wiki/spaces/{SPACE}/pages/{PAGE_ID}/{TITLE} | /wiki/x/{SHORT_ID}
→ mcp_atlassian_confluence_get_page(page_id, include_metadata=true, convert_to_markdown=true)

## §2 Detect Parent/Leaf
get_page_children(parent_id, limit=50, include_content=false)
children > 0 → PARENT → §3 | children = 0 → LEAF → §4

## §3 Recursive Children
```
readPageTree(pageId, depth, maxDepth):
  if depth > maxDepth: return []
  for child in get_page_children(pageId):
    content = get_page(child.id)
    results += readPageTree(child.id, depth+1, maxDepth)
```
Track VISITED_PAGES (Set) to avoid duplicates

## §4 Scan Links in Content
Match: [text](URL/pages/{ID}), /wiki/spaces/, <ac:link>, href patterns
Extract PAGE_IDs → LINKED_PAGES queue
If FOLLOW_LINKS: read each linked page (content only, !recurse children, !follow nested links)

## §5 Output
```
# Confluence Content Report
## Summary (root, type, counts)
## 📄 Root: {title}
## 📁 Children (nested by depth)
## 🔗 Linked Pages
```

## Error Handling
404 → skip | Permission denied → warn | Rate limit → wait 2s retry 1x | >50 pages → cap + warn

## Guardrails
- ALWAYS check VISITED_PAGES before reading
- MAX_DEPTH = 3 default
- Linked pages !recurse
- Max 50 pages per run
- Use mcp_atlassian_confluence_* tools — !browser
- include_metadata=true, convert_to_markdown=true
