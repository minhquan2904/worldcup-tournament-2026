---
name: wiki-readme-builder
description: Phân tích wiki index và backlinks, nhóm bài theo chủ đề, tạo Mermaid topic map và bảng thống kê cho README.md
allowed-tools: Read, Write, Edit, RunCommand
version: 1.0
---

# Wiki README Builder

> Skill chuyên phân tích cấu trúc wiki và render bản đồ kiến thức tổng quan cho README.md.

---

## Topic Clustering Rules

Phân loại bài wiki vào các domain dựa trên **article slug** (tên file) và **section trong _index.md** (concepts/tools/comparisons).

| Domain | Icon | Keywords trong slug |
|--------|------|-------------------|
| **Bảo mật & Kiểm soát Truy cập** | 🔐 | `abac`, `rbac`, `dac`, `mac`, `ngac`, `access-control`, `authentication`, `authorization` |
| **JavaScript & TypeScript** | ⚡ | `javascript`, `typescript`, `dom`, `rxjs`, `ngrx`, `clean-code-javascript`, `tsconfig`, `scope`, `closure` |
| **Java & Spring** | ☕ | `java`, `spring`, `jackson`, `jvm` |
| **Kiến trúc & Hệ thống** | 🏗️ | `kafka`, `rabbitmq`, `docker`, `nginx`, `n8n`, `message-broker`, `publish-subscribe`, `dependency-injection`, `generic-repository`, `state-pattern`, `command-pattern`, `composition`, `microservices` |
| **AI & LLM** | 🤖 | `rag`, `ollama`, `vllm`, `lm-studio`, `llama`, `phi-`, `gemma`, `anythingllm`, `smart-connections`, `continue-dev`, `antigravity`, `cognitive`, `socratic`, `sequential-multi`, `jagged`, `skill-leveling`, `ai-users`, `graph-rag`, `small-llm` |
| **Cơ sở dữ liệu** | 🗄️ | `oracle`, `acid`, `normalization`, `pl-sql`, `cost-based`, `analytic-functions`, `soft-delete`, `flashback`, `delete-vs-truncate`, `database` |
| **Frontend** | 🖥️ | `react`, `jotai`, `tanstack`, `virtual-dom` |

### Fallback Rule

- Bài nằm trong `comparisons/` → xét nội dung (dựa trên articles đang so sánh) để gán cluster
- Bài không match keyword nào → gán vào cluster **Khác**

---

## Hub Detection

| Threshold | Loại |
|-----------|------|
| ≥ 7 backlinks | **Super-hub** — đặt làm node chính của cluster |
| ≥ 4 backlinks | **Hub** — hiển thị trong diagram |
| < 4 backlinks | **Leaf** — chỉ đếm số lượng, không hiện từng bài |

---

## Mermaid Template

Dùng `mindmap` syntax (GitHub hỗ trợ native):

```
mindmap
  root((📚 LLM Wiki<br/>N bài · M liên kết))
    🔐 Bảo mật (X bài)
      Hub Article 1
      Hub Article 2
    ⚡ JavaScript (Y bài)
      ...
```

### Giới hạn
- Mermaid trên GitHub có giới hạn ~50 nodes. Nếu nhiều hơn → chỉ hiện hubs và super-hubs.
- Tên node dùng title tiếng Việt ngắn gọn (lấy từ summary hoặc alias).

---

## README Injection

### Markers
```html
<!-- WIKI-MAP:START -->
... nội dung auto-generated ...
<!-- WIKI-MAP:END -->
```

### Rules
1. Tìm markers trong README.md
2. Nếu có → replace nội dung giữa markers
3. Nếu không có → thêm section `## 🗺️ Bản Đồ Kiến Thức` trước section `## 🛠️ Công Nghệ Sử Dụng`
4. KHÔNG CHẠM vào nội dung ngoài markers

---

## Script

Chạy standalone:
```bash
python .agents/skills/wiki-readme-builder/scripts/build_topic_map.py
```

Script đọc `wiki/_index.md` + `wiki/_backlinks.json`, tự động generate và inject vào `README.md`.
