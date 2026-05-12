---
name: requirement-analysis
when_to_use: Analyze raw requirements — FR/NFR/BR/Constraints, extract hidden domain knowledge.
paths: [base_knowledge/standards/base/requirement-analysis/, base_knowledge/common_rules/PRJ-11-requirement-analysis-rule.md]
---

# Requirement Analysis & Knowledge Extraction

> Phân rã yêu cầu hỗn loạn → tài liệu chuẩn. Nghiệp vụ first, !DB design.

## Sub-Files
| File | When |
|------|------|
| PRJ-11-requirement-analysis-rule.md | BA thinking, traceability, hidden knowledge |
| openspec/schemas/modular_feature/templates/srs.md | SRS output template |

## Core Principles
- Phân mảnh → FR, NFR, BR, Constraints
- Tìm Hidden Knowledge: vòng đời, xóa mềm/cứng, audit
- Đánh giá rủi ro bảo mật + hiệu năng
- TUYỆT ĐỐI !thiết kế Data Model ở bước này

## Checklist
- [x] FR/NFR/BR rành mạch? | Mã định danh (FR-01)? | Góc khuất (status, auth, soft delete)?
- [x] Rủi ro bảo mật/hiệu năng? | Output khớp mẫu chuẩn?

## Anti-Patterns
❌ Tự ý thiết kế DB | ❌ Quên mã định danh | ❌ Bỏ qua rủi ro ẩn | ❌ Bỏ constraints
