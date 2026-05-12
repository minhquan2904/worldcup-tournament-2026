#!/usr/bin/env python3
"""
build_topic_map.py — Phân tích wiki, nhóm chủ đề, tạo Mermaid mindmap và cập nhật README.md

Chạy: python .agents/skills/wiki-readme-builder/scripts/build_topic_map.py
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ── Resolve project root ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent  # .agents/skills/wiki-readme-builder/scripts → root
WIKI_DIR = PROJECT_ROOT / "wiki"
INDEX_FILE = WIKI_DIR / "_index.md"
BACKLINKS_FILE = WIKI_DIR / "_backlinks.json"
README_FILE = PROJECT_ROOT / "README.md"

MARKER_START = "<!-- WIKI-MAP:START -->"
MARKER_END = "<!-- WIKI-MAP:END -->"

# ── Domain clustering rules ───────────────────────────────────────────
DOMAINS = {
    "🔐 Bảo mật & Kiểm soát Truy cập": {
        "keywords": [
            "abac", "rbac", "dac-vs-mac", "dac", "mac", "ngac",
            "access-control", "authentication", "authorization",
            "discretionary", "mandatory",
        ],
        "short": "Bảo mật",
    },
    "⚡ JavaScript & TypeScript": {
        "keywords": [
            "javascript", "typescript", "dom-", "rxjs", "ngrx",
            "clean-code-javascript", "tsconfig", "scope", "closure",
            "event-loop",
        ],
        "short": "JS/TS",
    },
    "☕ Java & Spring": {
        "keywords": [
            "java-", "spring-", "jackson", "jvm",
        ],
        "short": "Java/Spring",
    },
    "🏗️ Kiến trúc & Hệ thống": {
        "keywords": [
            "kafka", "rabbitmq", "docker", "nginx", "n8n",
            "message-broker", "publish-subscribe",
            "dependency-injection", "generic-repository",
            "state-pattern", "command-pattern",
            "composition-vs-inheritance", "microservices",
        ],
        "short": "Kiến trúc",
    },
    "🤖 AI & LLM": {
        "keywords": [
            "rag", "retrieval-augmented", "graph-rag",
            "ollama", "vllm", "lm-studio", "llama", "phi-",
            "gemma", "anythingllm", "smart-connections", "continue-dev",
            "antigravity", "cognitive", "socratic", "sequential-multi",
            "jagged", "skill-leveling", "ai-users", "small-llm",
        ],
        "short": "AI/LLM",
    },
    "🗄️ Cơ sở dữ liệu": {
        "keywords": [
            "oracle", "acid", "normalization", "pl-sql",
            "cost-based", "analytic-functions", "soft-delete",
            "flashback", "delete-vs-truncate", "database",
        ],
        "short": "Database",
    },
    "🖥️ Frontend": {
        "keywords": [
            "react-router", "jotai", "tanstack", "virtual-dom",
        ],
        "short": "Frontend",
    },
}

# ── Parse _index.md ───────────────────────────────────────────────────

def parse_index(index_path: Path) -> dict:
    """Parse _index.md, extract wiki articles grouped by section."""
    text = index_path.read_text(encoding="utf-8")
    articles = {}
    current_section = None

    # Match section headers: ## Concepts (N articles), ## Tools (N articles), etc.
    section_re = re.compile(r"^## (Concepts|Tools|People|Comparisons)", re.IGNORECASE)
    # Match table rows: | [[slug]] | aliases | summary |
    row_re = re.compile(
        r"\|\s*\[\[([^\]]+)\]\]\s*\|([^|]*)\|([^|]*)\|"
    )

    for line in text.splitlines():
        sec_match = section_re.match(line)
        if sec_match:
            current_section = sec_match.group(1).lower()
            continue
        if current_section and line.startswith("## "):
            # Hit a new non-article section (e.g. Raw Sources)
            current_section = None
            continue
        if current_section:
            row_match = row_re.search(line)
            if row_match:
                slug = row_match.group(1).strip()
                aliases = row_match.group(2).strip()
                summary = row_match.group(3).strip()
                articles[slug] = {
                    "section": current_section,
                    "aliases": aliases,
                    "summary": summary,
                }
    return articles


# ── Parse _backlinks.json ─────────────────────────────────────────────

def parse_backlinks(backlinks_path: Path) -> dict:
    """Return dict: slug → backlink_count (only wiki articles, not raw refs)."""
    data = json.loads(backlinks_path.read_text(encoding="utf-8"))
    bl = data.get("backlinks", {})
    counts = {}
    for target, sources in bl.items():
        # Filter: skip raw file refs (contain dots like '1.md', or paths)
        if "." in target or "/" in target or "#" in target:
            continue
        counts[target] = len(sources)
    return counts


# ── Classify articles into domains ────────────────────────────────────

def classify_articles(articles: dict) -> dict:
    """Assign each article to a domain. Returns {domain_name: [slugs]}."""
    clusters = defaultdict(list)
    unclassified = []

    for slug in articles:
        matched = False
        for domain, config in DOMAINS.items():
            for kw in config["keywords"]:
                if kw in slug:
                    clusters[domain].append(slug)
                    matched = True
                    break
            if matched:
                break
        if not matched:
            unclassified.append(slug)

    if unclassified:
        clusters["📦 Khác"] = unclassified

    return dict(clusters)


# ── Find hubs per cluster ─────────────────────────────────────────────

def find_hubs(clusters: dict, backlink_counts: dict, threshold: int = 4) -> dict:
    """Return {domain: [(slug, count)]} for articles with ≥ threshold backlinks."""
    hubs = {}
    for domain, slugs in clusters.items():
        domain_hubs = []
        for s in slugs:
            count = backlink_counts.get(s, 0)
            if count >= threshold:
                domain_hubs.append((s, count))
        domain_hubs.sort(key=lambda x: x[1], reverse=True)
        hubs[domain] = domain_hubs
    return hubs


# ── Sanitize Mermaid node text ────────────────────────────────────────

def mermaid_safe(text: str) -> str:
    """Remove or escape characters that break Mermaid syntax."""
    # Remove brackets, parentheses, quotes that Mermaid interprets
    text = text.replace('"', "'")
    text = text.replace("[", "").replace("]", "")
    text = text.replace("(", "").replace(")", "")
    text = text.replace("{", "").replace("}", "")
    text = text.replace("<", "").replace(">", "")
    text = text.replace("`", "")
    return text.strip()


def slug_to_label(slug: str, articles: dict) -> str:
    """Convert slug to short readable label."""
    art = articles.get(slug)
    if art:
        # Use first alias if short, otherwise prettify slug
        aliases = art["aliases"]
        if aliases:
            first = aliases.split(",")[0].strip()
            if len(first) <= 30:
                return mermaid_safe(first)
    # Fallback: prettify slug
    label = slug.replace("-", " ").title()
    if len(label) > 30:
        label = label[:27] + "..."
    return mermaid_safe(label)


# ── Generate Mermaid mindmap ──────────────────────────────────────────

def generate_mermaid(clusters: dict, hubs: dict, articles: dict,
                     backlink_counts: dict, total_articles: int,
                     total_links: int) -> str:
    """Generate Mermaid mindmap code."""
    lines = []
    lines.append("```mermaid")
    lines.append("mindmap")
    lines.append(f"  root((📚 LLM Wiki))")

    # Sort domains: largest cluster first
    sorted_domains = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)

    for domain, slugs in sorted_domains:
        count = len(slugs)
        short = DOMAINS.get(domain, {}).get("short", domain)
        icon = domain.split(" ")[0] if domain[0] != "📦" else "📦"
        lines.append(f"    {icon} {short} — {count} bài")

        # Show hubs (≥4 backlinks)
        domain_hubs = hubs.get(domain, [])
        shown = 0
        for slug, bl_count in domain_hubs:
            if shown >= 5:  # Max 5 hubs per domain to keep diagram clean
                break
            label = slug_to_label(slug, articles)
            lines.append(f"      {label}")
            shown += 1

        # If no hubs, show top 2 articles by backlink count
        if shown == 0:
            top = sorted(slugs, key=lambda s: backlink_counts.get(s, 0), reverse=True)[:2]
            for s in top:
                label = slug_to_label(s, articles)
                lines.append(f"      {label}")

    lines.append("```")
    return "\n".join(lines)


# ── Generate stats table ─────────────────────────────────────────────

def generate_stats_table(clusters: dict, hubs: dict, articles: dict,
                         total_articles: int, total_links: int) -> str:
    """Generate markdown stats table."""
    lines = []
    lines.append(f"> **{total_articles}** bài wiki · **{total_links}** liên kết chéo · "
                 f"Cập nhật: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("")
    lines.append("| Cluster | Bài | Hub Articles |")
    lines.append("|---------|-----|-------------|")

    sorted_domains = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)

    for domain, slugs in sorted_domains:
        count = len(slugs)
        domain_hubs = hubs.get(domain, [])
        if domain_hubs:
            hub_labels = ", ".join(
                f"**{slug_to_label(s, articles)}** ({c}↩)"
                for s, c in domain_hubs[:3]
            )
        else:
            hub_labels = "—"
        lines.append(f"| {domain} | {count} | {hub_labels} |")

    return "\n".join(lines)


# ── Inject into README.md ────────────────────────────────────────────

def inject_readme(readme_path: Path, content: str) -> bool:
    """Replace content between WIKI-MAP markers in README.md."""
    if not readme_path.exists():
        print(f"❌ README.md not found at {readme_path}")
        return False

    readme = readme_path.read_text(encoding="utf-8")

    if MARKER_START in readme and MARKER_END in readme:
        # Replace between markers
        start_idx = readme.index(MARKER_START) + len(MARKER_START)
        end_idx = readme.index(MARKER_END)
        new_readme = readme[:start_idx] + "\n" + content + "\n" + readme[end_idx:]
    else:
        # Insert before ## 🛠️ Công Nghệ Sử Dụng
        insert_marker = "## 🛠️ Công Nghệ Sử Dụng"
        section = (
            f"\n## 🗺️ Bản Đồ Kiến Thức\n\n"
            f"{MARKER_START}\n"
            f"{content}\n"
            f"{MARKER_END}\n\n"
        )
        if insert_marker in readme:
            new_readme = readme.replace(insert_marker, section + insert_marker)
        else:
            # Append at end
            new_readme = readme.rstrip() + "\n" + section

    readme_path.write_text(new_readme, encoding="utf-8")
    return True


# ── Main ──────────────────────────────────────────────────────────────

def main():
    print(f"📖 Đọc index tại: {INDEX_FILE}")
    if not INDEX_FILE.exists():
        print("❌ wiki/_index.md không tồn tại! Chạy /compile trước.")
        return

    articles = parse_index(INDEX_FILE)
    print(f"   → {len(articles)} bài wiki")

    # Backlinks
    total_links = 0
    backlink_counts = {}
    if BACKLINKS_FILE.exists():
        backlink_counts = parse_backlinks(BACKLINKS_FILE)
        bl_data = json.loads(BACKLINKS_FILE.read_text(encoding="utf-8"))
        total_links = bl_data.get("total_links", 0)
        print(f"   → {len(backlink_counts)} targets, {total_links} liên kết")
    else:
        print("⚠️  _backlinks.json không tồn tại, chạy không có backlink data")

    # Cluster
    clusters = classify_articles(articles)
    print(f"\n🗂️  Clusters:")
    for domain, slugs in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {domain}: {len(slugs)} bài")

    # Hubs
    hubs = find_hubs(clusters, backlink_counts, threshold=4)

    # Generate
    mermaid = generate_mermaid(clusters, hubs, articles, backlink_counts,
                               len(articles), total_links)
    stats = generate_stats_table(clusters, hubs, articles, len(articles), total_links)

    full_content = f"{mermaid}\n\n{stats}"

    # Inject
    print(f"\n📝 Cập nhật README.md...")
    success = inject_readme(README_FILE, full_content)
    if success:
        print(f"✅ README.md đã cập nhật với topic map!")
        print(f"   → {len(clusters)} clusters, {len(articles)} bài, {total_links} liên kết")
    else:
        print("❌ Không thể cập nhật README.md")


if __name__ == "__main__":
    main()
