---
title: "Dữ Liệu Lịch Sử Kết Quả Trận Đấu FIFA World Cup (1930–2022)"
source: "compiled"
date_added: 2026-05-12
tags: [data, worldcup, statistics, football, head-to-head, prediction]
aliases: [wc-match-data, lịch-sử-kết-quả-world-cup, fifa-historical-results]
status: draft
related:
  - "[[phan-tich-doi-dau-world-cup]]"
  - "[[mo-hinh-du-doan-world-cup-2026]]"
summary: "Tập dữ liệu 966 trận đấu tại FIFA World Cup 1930–2022 — cấu trúc, đặc điểm, và ứng dụng phân tích thống kê."
---

## Định Nghĩa

Bộ dữ liệu `clean_fifa_worldcup_historical_data.csv` là tập hợp kết quả 966 trận đấu chính thức tại FIFA World Cup trải dài từ kỳ đầu tiên (Uruguay, 1930) đến kỳ thứ 22 (Qatar, 2022). Mỗi bản ghi thể hiện một trận đấu với thông tin về hai đội tham gia, số bàn thắng mỗi bên, và năm tổ chức giải.

## Cấu Trúc Dữ Liệu

Tập dữ liệu có 6 cột:

| Cột | Kiểu | Mô tả |
|-----|------|--------|
| `home` | string | Đội tuyển đóng vai chủ nhà (theo phân bảng tournament, không theo địa lý) |
| `away` | string | Đội tuyển đóng vai khách |
| `year` | integer | Năm tổ chức World Cup |
| `home_goals` | integer | Số bàn thắng của đội home (nullable) |
| `away_goals` | integer | Số bàn thắng của đội away (nullable) |
| `total_goals` | integer | Tổng bàn thắng trong trận (nullable nếu hai cột trên null) |

Thuật ngữ "home" và "away" trong bộ dữ liệu phản ánh vị trí phân nhóm bảng đấu, không phải lợi thế sân nhà theo nghĩa địa lý truyền thống. Phần lớn các trận đấu tại World Cup không có đội sân nhà thực sự (trừ đội chủ nhà tổ chức).

## Phạm Vi Và Đặc Điểm

### Phạm Vi Thời Gian

22 kỳ World Cup: **1930 · 1934 · 1938 · 1950 · 1954 · 1958 · 1962 · 1966 · 1970 · 1974 · 1978 · 1982 · 1986 · 1990 · 1994 · 1998 · 2002 · 2006 · 2010 · 2014 · 2018 · 2022**

Tổng cộng **966 trận**. Số trận mỗi kỳ tăng dần theo thời gian do mở rộng số đội tham dự: từ 13 đội (1930) lên 32 đội (1998–2022).

### Tên Đội Tuyển Lịch Sử

Dữ liệu giữ nguyên tên đội theo đúng thời điểm lịch sử. Một số tên đội tuyển đã biến mất hoặc thay đổi sau khi các quốc gia tan rã hoặc thống nhất:

- **West Germany** (1954–1990) → thay thế bởi **Germany** (từ 1994)
- **East Germany** — tham dự 1974 duy nhất một lần
- **Soviet Union** — tham dự đến 1990, sau đó tan rã
- **FR Yugoslavia** — tên dùng trong 1998 sau khi Yugoslavia phân tách
- **Czechoslovakia** — tham dự đến 1990, tách thành Czech Republic và Slovakia từ 1993
- **Dutch East Indies** — đại diện vùng lãnh thổ Đông Ấn Hà Lan tại World Cup 1938

Khi phân tích đối đầu giữa các quốc gia có tên thay đổi, cần ánh xạ tên cũ về tên quốc gia hiện tại trước khi tính tổng hợp.

### Dữ Liệu Thiếu (Nullable)

Trận **Sweden vs Austria** (1938) có `home_goals` và `away_goals` để trống. Austria rút khỏi giải sau khi bị Đức sáp nhập (Anschluss), Sweden được đi tiếp mà không cần thi đấu. Đây là trường hợp duy nhất trong dataset có giá trị null.

## Ứng Dụng Phân Tích

### Thống Kê Đơn Giản

Từ bộ dữ liệu có thể tính trực tiếp:
- Số trận thắng/hoà/thua của từng đội tuyển qua các kỳ World Cup
- Số bàn thắng trung bình mỗi trận theo từng thập kỷ
- Tỉ lệ thắng của đội home trong từng giai đoạn

### Phân Tích Đối Đầu (Head-to-Head)

Gộp theo cặp `(home, away)` và `(away, home)` cho phép tính lịch sử trực tiếp giữa hai đội. Ví dụ: Brazil và Germany gặp nhau 9 lần trong lịch sử World Cup, kết quả trận 1–7 năm 2014 tại Belo Horizonte là một điểm dữ liệu nằm trong bộ này (`Brazil,Germany,2014,1,7,8`).

### Mô Hình Dự Đoán

Bộ dữ liệu là nền tảng phổ biến cho các mô hình dự đoán kết quả World Cup. Hai hướng tiếp cận chính:
1. **Phương pháp thống kê cổ điển** — Poisson regression dựa trên tỉ lệ bàn thắng lịch sử.
2. **Machine learning** — Gradient boosting hoặc neural network với features bổ sung (FIFA ranking, vị trí địa lý, thành tích vòng loại).

Bộ dữ liệu này tương thích với các pipeline phân tích cho [[mo-hinh-du-doan-world-cup-2026]].

## Giới Hạn

Bộ dữ liệu chỉ ghi nhận kết quả sau 90 phút chính thức. Kết quả hiệp phụ, loạt sút penalty không được phân biệt riêng — các trận kết thúc bằng penalty (ví dụ: Brazil vs Italy 1994 chung kết, ghi là `0,0`) không phản ánh đội chiến thắng thực tế trong cột `home_goals`/`away_goals`.

Bộ dữ liệu không bao gồm các thông tin bổ trợ như: đội hình ra sân, số thẻ phạt, thống kê cá nhân cầu thủ, hay điều kiện thời tiết.

## Nguồn Tham Khảo

- Dữ liệu gốc: `raw/misc/clean_fifa_worldcup_historical_data.csv`
- Xem thêm: [[phan-tich-doi-dau-world-cup]] · [[mo-hinh-du-doan-world-cup-2026]]
