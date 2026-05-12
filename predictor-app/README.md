# WC2026 AI Predictor — Web App

Web app dự đoán kết quả các trận đấu FIFA World Cup 2026 bằng AI, build từ dữ liệu trong cùng repo này (`raw/misc/` + `wiki/concepts/`).

## Mở app

- **Landing page**: mở `landing.html` (giới thiệu sản phẩm)
- **App dự đoán**: mở `index.html` (predictor chính)

Đều là file HTML tĩnh — double-click là chạy. Không cần build, không cần server.

## Tính năng

- 48 đội × 12 bảng A–L theo bốc thăm chính thức 5/12/2025
- 72 trận vòng bảng với Match # đúng lịch FIFA
- Mỗi trận có nút **🤖 AI dự đoán** → Gemini 2.5 Flash phân tích, trả về:
  - Xác suất 3 chiều (thắng / hòa / thắng) cộng = 100%
  - Tỉ số dự đoán + mức độ tự tin
  - 3 đoạn phân tích tiếng Việt: Phong độ / Lịch sử / Dự đoán
  - 3 yếu tố then chốt
- Drill-down **📊 Dữ liệu AI đã dùng** — xem được số liệu thô AI dùng để dự đoán
- Bảng xếp hạng dự kiến tự sinh sau khi dự đoán đủ 6 trận của 1 bảng
- Lưu predictions trong `localStorage` — refresh không mất

## Methodology — "Hybrid Stat + LLM Reasoning"

AI dự đoán dựa trên 3 tầng:

### Tầng 1 — Stats từ 966 trận WC lịch sử (1930–2022)
- Head-to-Head: số trận gặp nhau, win/draw/loss, tổng bàn, kết quả gần nhất
- Time-decayed win rate: trận gần đây trọng số cao hơn (`decay = 0.95^(2026 - year)`)
- Sức mạnh toàn thời WC mỗi đội: số kỳ tham dự, win rate, trung bình bàn

### Tầng 2 — Bối cảnh metadata
- Số chức vô địch WC (Brazil 5, Đức 4, Ý 4, Argentina 3, Pháp 2, Uruguay 2, Anh 1, TBN 1)
- Lợi thế chủ nhà 🇺🇸 🇨🇦 🇲🇽
- FIFA ranking tier (1–4)
- Liên đoàn (UEFA / CONMEBOL / CAF / AFC / CONCACAF / OFC)

### Tầng 3 — Gemini synthesis
Nhận đầy đủ data từ Tầng 1 + 2 + tri thức về phong độ 2024–2026, ngôi sao chủ chốt, HLV, lối chơi → output JSON có cấu trúc.

## Cách dùng

1. Mở `landing.html` (xem MKT) hoặc trực tiếp `index.html`
2. Lấy Gemini API key miễn phí: https://aistudio.google.com/apikey
3. Click ⚙️ Settings (góc trên phải), dán key, lưu
4. Click nút **🤖 AI** trên bất kỳ trận nào, hoặc **"Dự đoán toàn vòng bảng"** để chạy hết 72 trận

## Tech stack

- HTML5 + Tailwind CSS (CDN) + Vanilla JS
- Google Fonts: Outfit (display) + Work Sans (body)
- Gemini 2.5 Flash via REST (`generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent`)
- 964 trận lịch sử embed inline (~50KB) — offline-ready
- `localStorage` cho API key + prediction cache

## Data sources

Dữ liệu được lấy từ chính repo này:
- `raw/misc/clean_fifa_worldcup_historical_data.csv` — 966 trận WC 1930–2022
- `raw/misc/format_fixture_data.csv` — 104 trận WC 2026 với match number
- `wiki/concepts/bang-dau-worldcup-2026.md` — 12 bảng A–L, 48 đội

## Tham khảo

- [[../wiki/concepts/du-lieu-lich-su-ket-qua-worldcup]]
- [[../wiki/concepts/phan-tich-doi-dau-world-cup]]
- [[../wiki/concepts/bang-dau-worldcup-2026]]
- [[../wiki/concepts/cau-truc-giai-dau-worldcup-2026]]
