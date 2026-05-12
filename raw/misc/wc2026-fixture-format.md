---
title: "FIFA World Cup 2026 — Lịch Thi Đấu Đầy Đủ (48 Đội, 12 Bảng)"
source: "d:/9. Learn/16. wc2026/worldcup-tournament-2026/temp/format_fixture_data.csv"
date_added: 2026-05-12
tags: [data, worldcup, wc2026, fixture, schedule, tournament-bracket, groups]
aliases: [wc2026-fixture-format, lịch-thi-đấu-đầy-đủ-2026, 48-teams-wc2026]
status: draft
summary: "Lịch thi đấu FIFA World Cup 2026 với 48 đội đã điền đầy đủ vào 12 bảng A–L — 104 trận từ vòng bảng đến chung kết."
---

## Mô Tả Dữ Liệu

File `format_fixture_data.csv` là lịch thi đấu **đã format đầy đủ** của FIFA World Cup 2026, với 48 đội tuyển được phân bổ vào 12 bảng (A–L). Đây là dữ liệu **dự kiến/simulation** — phản ánh bốc thăm/dự đoán phân bổ đội vào các slot còn trống trong fixture gốc.

**File gốc:** `format_fixture_data.csv`  
**Vị trí:** `raw/misc/format_fixture_data.csv`  
**Xem thêm:** [[wc2026-fixture-raw]] (skeleton chỉ có 3 đội đăng cai)

### Cấu Trúc Dữ Liệu

| Cột | Kiểu | Mô tả |
|-----|------|--------|
| `home` | string | Tên đội tuyển phía home |
| `score` | string | Mã trận đấu (Match 1 → Match 104) |
| `away` | string | Tên đội tuyển phía away |
| `year` | integer | Năm tổ chức (2026) |

### Phân Bổ 48 Đội Vào 12 Bảng

| Bảng | Đội 1 | Đội 2 | Đội 3 | Đội 4 |
|------|-------|-------|-------|-------|
| **A** | Mexico | Chile | Saudi Arabia | Peru |
| **B** | Canada | Denmark | Iran | Mali |
| **C** | Argentina | Belgium | Egypt | Cape Verde |
| **D** | United States | Morocco | Ecuador | New Zealand |
| **E** | Brazil | Switzerland | Tunisia | Nigeria |
| **F** | France | Senegal | Uzbekistan | Austria |
| **G** | Portugal | South Korea | South Africa | Panama |
| **H** | England | Italy | Paraguay | Turkey |
| **I** | Spain | Japan | Qatar | Scotland |
| **J** | Germany | Colombia | Ghana | Jordan |
| **K** | Croatia | Australia | Ivory Coast | Serbia |
| **L** | Netherlands | Uruguay | Algeria | Poland |

### Cấu Trúc Trận Đấu

**Vòng bảng (Match 1–72):** Mỗi bảng thi đấu vòng tròn 1 lượt, 6 trận/bảng × 12 bảng = 72 trận.

**Vòng 1/8 (Match 73–88):** 16 trận — nhất, nhì mỗi bảng + 8 đội hạng ba tốt nhất.

**Vòng tứ kết (Match 89–96):** 8 trận.

**Vòng bán kết (Match 97–100 + 101–102):** 4 trận.

**Hạng ba (Match 103):** Hai đội thua bán kết.

**Chung kết (Match 104):** Hai đội thắng bán kết.

### Đặc Điểm Nổi Bật Trong Phân Bổ

- **3 nước đồng đăng cai** (Mexico, Canada, USA) được xếp vào 3 bảng khác nhau (A, B, D) — đảm bảo không gặp nhau trước vòng loại trực tiếp.
- **Uzbekistan** (Bảng F) là đại diện Trung Á hiếm gặp tại World Cup, phản ánh sự mở rộng lên 48 đội.
- **Cape Verde, Mali, Jordan** — các đội lần đầu hoặc hiếm khi tham dự World Cup, tiêu biểu cho thời đại 48 đội.
- **Qatar** (Bảng I) tham dự với tư cách đội thường dù đã là chủ nhà WC 2022.

### Ứng Dụng

File này là input chính cho:
- Tính toán **head-to-head lịch sử** từng cặp đội trong cùng bảng
- Xây dựng **mô hình dự đoán** kết quả vòng bảng và vòng loại trực tiếp
- Phân tích **độ khó bảng đấu** (group difficulty) dựa trên FIFA ranking
- Liên kết với [[du-lieu-lich-su-ket-qua-worldcup]] để tra cứu đối đầu lịch sử giữa các cặp đội trong cùng bảng

## Nguồn Gốc

Dữ liệu được tạo dựa trên cấu trúc bracket FIFA World Cup 2026 chính thức, với các đội tuyển được phân bổ dựa trên kết quả vòng loại và bốc thăm dự kiến.
