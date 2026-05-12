---
title: "FIFA World Cup 2026 — Lịch Thi Đấu Gốc (Skeleton Fixture)"
source: "d:/9. Learn/16. wc2026/worldcup-tournament-2026/temp/fifa_worldcup_fixture.csv"
date_added: 2026-05-12
tags: [data, worldcup, wc2026, fixture, schedule, tournament-bracket]
aliases: [wc2026-fixture, lịch-thi-đấu-wc2026, fixture-2026-skeleton]
status: draft
summary: "Lịch thi đấu skeleton của FIFA World Cup 2026 — 105 trận, chỉ 3 đội đăng cai đã xác định (Mexico, Canada, USA), còn lại là slot placeholder theo bảng đấu."
---

## Mô Tả Dữ Liệu

File `fifa_worldcup_fixture.csv` là lịch thi đấu **chính thức dạng skeleton** của FIFA World Cup 2026. Đây là cấu trúc bracket của giải đấu trước khi vòng bốc thăm xác định đầy đủ các đội.

**File gốc:** `fifa_worldcup_fixture.csv`  
**Vị trí:** `raw/misc/fifa_worldcup_fixture.csv`

### Cấu Trúc Dữ Liệu

| Cột | Kiểu | Mô tả |
|-----|------|--------|
| `home` | string | Đội tuyển / slot placeholder phía home |
| `score` | string | Mã trận đấu (Match 1 → Match 104) |
| `away` | string | Đội tuyển / slot placeholder phía away |
| `year` | integer | Năm tổ chức (2026) |

### Thống Kê Tổng Quan

- **Tổng số trận:** 104 trận (Match 1 → Match 104)
- **Vòng bảng:** Match 1–72 (12 bảng × 6 trận)
- **Vòng 1/8:** Match 73–88 (16 trận)
- **Vòng tứ kết:** Match 89–96 (8 trận)
- **Vòng bán kết:** Match 97–100 (4 trận)
- **Hạng ba:** Match 103
- **Chung kết:** Match 104

### Đội Tuyển Đã Xác Định

Chỉ 3 đội đăng cai đã được điền cố định:
- **Mexico** — Bảng A (Match 1, 28, 53)
- **Canada** — Bảng B (Match 3, 27, 51)
- **United States** — Bảng D (Match 4, 32, 59)

Tất cả slot còn lại (A2, A3, A4, B2, B3, B4, D2, D3, D4…) và các bảng C, E–L hoàn toàn trống (`null`).

### Cấu Trúc Vòng Loại Trực Tiếp

World Cup 2026 mở rộng lên **48 đội**, tổ chức theo 12 bảng (A–L), mỗi bảng 4 đội. Vòng loại trực tiếp gồm 32 đội: nhất và nhì mỗi bảng (24 đội) + 8 đội hạng ba tốt nhất.

File này thể hiện cấu trúc bracket với logic `Winner Group X`, `Runner-up Group X`, `3rd Group X/Y/Z/...` cho các trận từ vòng 1/8 trở đi.

### Lưu Ý

- Các trận có `home` và `away` đều null là các slot chưa biết đội thi đấu.
- File này là **cấu trúc bracket**, không phải lịch thi đấu theo ngày/giờ/địa điểm.
- Xem [[wc2026-fixture-format]] để có phiên bản đầy đủ với tên đội giả định.

## Nguồn Gốc

Dữ liệu phản ánh cấu trúc giải đấu FIFA World Cup 2026 dựa trên thông tin chính thức từ FIFA.
