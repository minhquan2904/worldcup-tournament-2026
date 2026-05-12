---
description: Tạo bản đồ kiến thức tổng quan từ wiki index và cập nhật README.md
---

# /overview — Tạo Bản Đồ Kiến Thức Tổng Quan

Workflow này phân tích cấu trúc wiki, nhóm bài theo chủ đề, vẽ Mermaid topic map và cập nhật README.md — giúp xem tổng quan wiki trực tiếp trên GitHub.

## Kích Hoạt

- `/overview`
- `/update-readme`
- "Cập nhật bản đồ wiki"
- "Update topic map"

## Bước Thực Hiện

### 1. Chạy script tự động

// turbo
```bash
python .agents/skills/wiki-readme-builder/scripts/build_topic_map.py
```

Script sẽ tự động:
- Đọc `wiki/_index.md` và `wiki/_backlinks.json`
- Nhóm bài theo 7 domain (Bảo mật, JS/TS, Java/Spring, Kiến trúc, AI/LLM, Database, Frontend)
- Xác định hub articles (bài có nhiều backlinks nhất)
- Generate Mermaid mindmap + bảng thống kê
- Inject vào README.md giữa markers `<!-- WIKI-MAP:START -->` / `<!-- WIKI-MAP:END -->`

### 2. Review kết quả

// turbo
Đọc README.md, kiểm tra:
- Mermaid diagram có đúng cấu trúc không
- Bảng thống kê có chính xác không
- Không phá vỡ phần khác của README

### 3. Báo cáo

```
🗺️ Bản đồ wiki đã cập nhật!

### Thống kê:
- Tổng bài: [N]
- Tổng liên kết: [M]
- Clusters: [K]

### Clusters:
| Domain | Bài | Hubs |
|--------|-----|------|
| ...    | ... | ...  |

📄 README.md đã sẵn sàng push lên GitHub.
```

### 4. Append Operations Log

// turbo
Append vào `wiki/_ops_log.md`:
```markdown
## [YYYY-MM-DD] overview | Cập nhật topic map README — N bài, M liên kết
```

## Quy Tắc

1. **Script-first:** Luôn chạy Python script trước, chỉ sửa thủ công nếu script lỗi
2. **Idempotent:** Chạy bao nhiêu lần cũng cho kết quả nhất quán
3. **Non-destructive:** Chỉ thay nội dung giữa markers, không đụng phần khác

## Xử Lý Lỗi

| Tình huống | Cách xử lý |
|-----------|------------|
| `_index.md` không tồn tại | Báo lỗi, yêu cầu chạy `/compile` trước |
| `_backlinks.json` không tồn tại | Chạy `python wiki/_build_backlinks.py` trước |
| Markers không có trong README | Thêm markers + section mới |
| Mermaid quá lớn (>50 nodes) | Chỉ hiện hubs, ẩn leaf articles |
