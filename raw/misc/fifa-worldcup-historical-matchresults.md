---
title: "FIFA World Cup — Kết Quả Đối Đầu Lịch Sử Các Đội Tuyển (1930–2022)"
source: "d:/9. Learn/16. wc2026/worldcup-tournament-2026/temp/clean_fifa_worldcup_historical_data.csv"
date_added: 2026-05-12
tags: [data, football, worldcup, statistics, head-to-head]
aliases: [wc-match-history, fifa-historical-data, đối-đầu-world-cup]
status: draft
summary: "Tập dữ liệu 966 trận đấu tại FIFA World Cup từ 1930 đến 2022 — home team, away team, năm, số bàn thắng mỗi đội."
related:
  - "[[fifa-worldcup-2026]]"
---

## Mô Tả Dữ Liệu

Tập dữ liệu ghi nhận kết quả thi đấu tại **FIFA World Cup** từ kỳ đầu tiên năm 1930 đến kỳ 2022 tại Qatar.

**File gốc:** `clean_fifa_worldcup_historical_data.csv`  
**Vị trí:** `raw/misc/clean_fifa_worldcup_historical_data.csv`

### Cấu Trúc Dữ Liệu

| Cột | Kiểu | Mô tả |
|-----|------|--------|
| `home` | string | Tên đội tuyển đóng vai chủ nhà (theo phân nhóm tournament) |
| `away` | string | Tên đội tuyển đóng vai khách |
| `year` | integer | Năm tổ chức World Cup |
| `home_goals` | integer | Số bàn thắng của đội home (có thể null — trận huỷ/bỏ thi đấu) |
| `away_goals` | integer | Số bàn thắng của đội away (có thể null) |
| `total_goals` | integer | Tổng bàn thắng trong trận |

### Thống Kê Tổng Quan

- **Tổng số trận:** 966 trận
- **Phạm vi thời gian:** 1930–2022 (20 kỳ World Cup)
- **Số đội tuyển xuất hiện:** > 80 quốc gia

### Các Kỳ World Cup Có Trong Dữ Liệu

1930 · 1934 · 1938 · 1950 · 1954 · 1958 · 1962 · 1966 · 1970 · 1974 · 1978 · 1982 · 1986 · 1990 · 1994 · 1998 · 2002 · 2006 · 2010 · 2014 · 2018 · 2022

### Lưu Ý Về Dữ Liệu

- Trận **Sweden vs Austria (1938)** có `home_goals` và `away_goals` để trống — Austria rút khỏi giải sau khi bị Đức併合, Sweden được đi tiếp mà không thi đấu.
- Tên đội tuyển phản ánh tên lịch sử tại thời điểm thi đấu: `West Germany` (trước 1991), `East Germany`, `Soviet Union`, `FR Yugoslavia`, `Czechoslovakia`, `Dutch East Indies`...
- Kết quả **sau 90 phút chính thức** — không bao gồm hiệp phụ/penalty nếu trận kết thúc hoà ở vòng đấu loại trực tiếp.

### Ứng Dụng Phân Tích

- Tính toán **win rate** theo từng cặp đội đối đầu
- Thống kê **số bàn thắng trung bình** theo kỳ World Cup / theo đội
- Xây dựng **mô hình dự đoán** cho World Cup 2026
- Phân tích **xu hướng** bàn thắng qua các thập kỷ

## Nguồn Gốc

Dữ liệu đã được clean và chuẩn hoá từ kết quả lịch sử FIFA World Cup.
Tên file gốc: `clean_fifa_worldcup_historical_data.csv`
