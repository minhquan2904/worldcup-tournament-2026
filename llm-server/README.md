# LLM Server — Guideline

> Shared LLM Service chạy local. Mọi dự án/tool trong tổ chức đều gọi chung endpoint duy nhất.

---

## Mục lục

1. [Tổng quan kiến trúc](#1-tổng-quan-kiến-trúc)
2. [Quick Start](#2-quick-start)
3. [Cấu trúc thư mục](#3-cấu-trúc-thư-mục)
4. [Cấu hình (.env)](#4-cấu-hình-env)
5. [Model Management](#5-model-management)
6. [Health Check](#6-health-check)
7. [Backup & Restore](#7-backup--restore)
8. [Kết nối từ các service](#8-kết-nối-từ-các-service)
9. [Optional: Reverse Proxy](#9-optional-reverse-proxy)
10. [Optional: Monitoring](#10-optional-monitoring)
11. [So sánh & chọn model](#11-so-sánh--chọn-model)
12. [Performance Tuning](#12-performance-tuning)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│ HOST MACHINE                                            │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ llm-server (Docker)                              │    │
│  │                                                  │    │
│  │  ┌──────────┐   ┌──────────┐   ┌────────────┐  │    │
│  │  │ Ollama   │   │ Models   │   │ Nginx      │  │    │
│  │  │ Runtime  │   │ (Volume) │   │ (Optional) │  │    │
│  │  │ :11434   │   │ 2-20GB   │   │ :11435     │  │    │
│  │  └──────────┘   └──────────┘   └────────────┘  │    │
│  └────────────────────┬────────────────────────────┘    │
│                       │ port 11434                       │
├───────────────────────┼─────────────────────────────────┤
│                       │                                  │
│  Consumers:           │                                  │
│  • MCP Test Agent ────┘ (http://host.docker.internal)    │
│  • IDE (Continue.dev) ─── (http://localhost)              │
│  • Python scripts ────── (http://localhost)               │
│  • Team LAN ──────────── (http://192.168.x.x)            │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Nguyên tắc:**
- Ollama là implementation detail — client chỉ cần biết URL + model name
- Một nơi quản lý model, nhiều nơi sử dụng
- Không có authentication mặc định (dùng Nginx proxy nếu cần)

---

## 2. Quick Start

```powershell
# 1. Khởi động
cd llm-server/
docker compose up -d

# 2. Kiểm tra (chờ model pull xong)
.\scripts\health-check.ps1

# 3. Test nhanh
curl http://localhost:11434/api/chat -d '{
  "model": "qwen2.5-coder:3b",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": false
}'
```

Lần đầu mất 2-5 phút để pull model. Các lần sau khởi động trong vài giây.

---

## 3. Cấu trúc thư mục

```
llm-server/
├── docker-compose.yml       # Container definition + optional profiles
├── .env                     # Cấu hình (model, port, limits)
├── nginx/                   # [profile: proxy]
│   └── nginx.conf           # Reverse proxy config
├── monitoring/              # [profile: monitoring]
│   └── prometheus.yml       # Prometheus scrape config
├── scripts/
│   ├── manage-models.ps1    # Quản lý models
│   ├── health-check.ps1     # Kiểm tra trạng thái
│   └── backup-models.ps1    # Backup/restore volume
├── backups/                 # Thư mục chứa backup (auto-created)
├── README.md                # Guideline (file này)
└── CONNECTION-GUIDE.md      # Hướng dẫn kết nối chi tiết
```

---

## 4. Cấu hình (.env)

| Biến | Mặc định | Mô tả |
|------|----------|-------|
| `LLM_MODELS` | `qwen2.5-coder:3b` | Model(s) pull khi khởi động. Nhiều model cách space |
| `LLM_PORT` | `11434` | Port expose ra host |
| `OLLAMA_NUM_PARALLEL` | `2` | Requests xử lý đồng thời |
| `OLLAMA_MAX_LOADED_MODELS` | `1` | Models giữ trong VRAM cùng lúc |
| `LLM_MEMORY_LIMIT` | `8g` | Giới hạn RAM container |
| `PROXY_PORT` | `11435` | Port cho Nginx proxy (profile: proxy) |
| `PROXY_API_KEY` | — | API key cho proxy auth |
| `PROMETHEUS_PORT` | `9090` | Port Prometheus (profile: monitoring) |
| `GRAFANA_PORT` | `3000` | Port Grafana (profile: monitoring) |
| `GRAFANA_PASSWORD` | `admin` | Grafana admin password |

### Ví dụ: chạy 2 model (code + chat)

```env
LLM_MODELS=qwen2.5-coder:3b qwen2.5:3b
OLLAMA_MAX_LOADED_MODELS=1    # Chỉ giữ 1 trong VRAM, swap khi cần
```

---

## 5. Model Management

```powershell
# Xem models đã cài
.\scripts\manage-models.ps1 list

# Pull model mới
.\scripts\manage-models.ps1 pull qwen2.5-coder:7b

# Xoá model (giải phóng disk)
.\scripts\manage-models.ps1 remove qwen2.5-coder:3b

# Xem chi tiết model
.\scripts\manage-models.ps1 info qwen2.5-coder:3b

# Xem model đang loaded trong VRAM
.\scripts\manage-models.ps1 running
```

### Pull thủ công qua Docker

```powershell
docker exec llm-server ollama pull qwen2.5-coder:7b
docker exec llm-server ollama list
docker exec llm-server ollama rm qwen2.5-coder:3b
```

---

## 6. Health Check

```powershell
.\scripts\health-check.ps1
```

Output:
```
🔍 LLM Server Health Check
==================================================

[1/5] Docker container... ✅ Running (Up 2 hours (healthy))
[2/5] API endpoint...     ✅ Accessible (http://localhost:11434)
[3/5] GPU...              ✅ NVIDIA RTX 4050 — VRAM: 2048/6144 MB
[4/5] Models installed... ✅ 1 model(s)
     • qwen2.5-coder:3b (1.9GB)
[5/5] Inference test...   ✅ Response received

==================================================
✅ LLM Server is healthy!
```

---

## 7. Backup & Restore

Models tốn 2-5GB và mất thời gian download. Backup volume để tránh re-pull:

```powershell
# Backup
.\scripts\backup-models.ps1 backup
# → backups/ollama-models-20260425-220700.tar.gz (1.9GB)

# Restore (từ backup mới nhất)
.\scripts\backup-models.ps1 restore
```

---

## 8. Kết nối từ các service

| Từ đâu | URL |
|--------|-----|
| Máy host (local) | `http://localhost:11434` |
| Docker container cùng host | `http://host.docker.internal:11434` |
| Máy khác trong LAN | `http://<HOST_IP>:11434` |

Chi tiết xem [CONNECTION-GUIDE.md](CONNECTION-GUIDE.md).

---

## 9. Optional: Reverse Proxy

Nginx proxy thêm lớp bảo vệ khi mở LAN:

| Tính năng | Mô tả |
|-----------|-------|
| **API Key auth** | Client gửi header `X-API-Key` |
| **Rate limiting** | 10 req/phút per IP |
| **Request size** | Max 10MB |
| **CORS** | Tự động thêm headers |
| **Timeouts** | 5 phút cho inference |

### Bật proxy

```powershell
# 1. Set API key
# Sửa .env → bỏ comment PROXY_API_KEY

# 2. Khởi động với profile proxy
docker compose --profile proxy up -d

# 3. Client gọi qua proxy port
curl -H "X-API-Key: your-key" http://localhost:11435/api/chat -d '{...}'
```

### Khi nào nên dùng proxy?

| Scenario | Dùng proxy? |
|----------|-------------|
| Chỉ dùng local 1 mình | ❌ Không cần |
| Team nội bộ tin tưởng | ❌ Không cần |
| Mở cho nhiều team/phòng ban | ✅ Rate limit |
| Expose ra internet | ✅ Bắt buộc (auth + rate limit) |

---

## 10. Optional: Monitoring

Prometheus + Grafana để giám sát LLM Server.

| Service | Port | Mô tả |
|---------|------|-------|
| **Prometheus** | 9090 | Thu thập metrics, health probes |
| **Grafana** | 3000 | Dashboard visualize |

### Bật monitoring

```powershell
# Khởi động kèm monitoring
docker compose --profile monitoring up -d

# Truy cập
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000 (admin / admin)
```

### Tắt monitoring

```powershell
docker compose --profile monitoring stop prometheus grafana
```

### Bật tất cả optional features

```powershell
docker compose --profile proxy --profile monitoring up -d
```

### Khi nào nên dùng monitoring?

| Scenario | Dùng? |
|----------|-------|
| Dev 1 mình | ❌ Không cần |
| Team nhỏ, dùng ít | ❌ Health check script đủ |
| Nhiều user, chạy 24/7 | ✅ Theo dõi uptime |
| Debug performance | ✅ Xem VRAM/request patterns |

---

## 11. So sánh & chọn model

### Qwen2.5-Coder (Khuyến nghị cho code generation)

| Model | VRAM (Q4) | Tốc độ | Chất lượng | Phù hợp |
|-------|-----------|--------|-----------|---------|
| `qwen2.5-coder:0.5b` | ~0.5 GB | ⚡⚡⚡⚡⚡ | ⭐ | FIM/autocomplete |
| `qwen2.5-coder:1.5b` | ~1.2 GB | ⚡⚡⚡⚡ | ⭐⭐ | Code completion |
| **`qwen2.5-coder:3b`** | **~2.5 GB** | **⚡⚡⚡** | **⭐⭐⭐** | **GPU 6GB chia sẻ** |
| `qwen2.5-coder:7b` | ~5 GB | ⚡⚡ | ⭐⭐⭐⭐ | GPU 8GB+ chuyên dụng |
| `qwen2.5-coder:14b` | ~10 GB | ⚡ | ⭐⭐⭐⭐⭐ | GPU 12-16GB |
| `qwen2.5-coder:32b` | ~20 GB | 🐢 | ⭐⭐⭐⭐⭐+ | GPU 24GB, ngang GPT-4o |

### Chọn theo GPU

| GPU VRAM | Model khuyến nghị | Lý do |
|----------|-------------------|-------|
| 4 GB | `qwen2.5-coder:1.5b` | Fit vừa |
| **6 GB (chia sẻ)** | **`qwen2.5-coder:3b`** | **2.5GB + còn cho công việc** |
| 6 GB (chuyên dụng) | `qwen2.5-coder:7b` | Chiếm gần hết nhưng tốt hơn |
| 8 GB | `qwen2.5-coder:7b` | Sweet spot |
| 12-16 GB | `qwen2.5-coder:14b` | Gần ngang thương mại |
| 24 GB | `qwen2.5-coder:32b` | Ngang GPT-4o |

Chi tiết đầy đủ xem [README.md](README.md).

---

## 12. Performance Tuning

### VRAM không đủ

```env
# Giảm parallel requests
OLLAMA_NUM_PARALLEL=1

# Giảm context window (chạy trong container)
docker exec llm-server ollama run qwen2.5-coder:3b --num-ctx 4096
```

### Muốn response nhanh hơn

```env
# Dùng model nhỏ hơn
LLM_MODELS=qwen2.5-coder:1.5b

# Hoặc tăng parallel (nếu đủ VRAM)
OLLAMA_NUM_PARALLEL=4
```

### Multi-model (code + chat)

```env
LLM_MODELS=qwen2.5-coder:3b qwen2.5:3b
OLLAMA_MAX_LOADED_MODELS=1    # Swap model khi cần (chậm hơn lần đầu)
# Hoặc =2 nếu đủ VRAM giữ cả 2
```

---

## 13. Troubleshooting

| Vấn đề | Nguyên nhân | Fix |
|--------|-------------|-----|
| `Connection refused` | Container chưa start | `docker compose up -d` |
| `Model not found` | Chưa pull model | `.\scripts\manage-models.ps1 pull <model>` |
| `OOM / out of memory` | Model quá lớn | Đổi model nhỏ hơn trong `.env` |
| `0% GPU` | nvidia-container-toolkit chưa cài | [Hướng dẫn](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) |
| Chậm bất thường | Context quá lớn hoặc swap model | Giảm `num_ctx` hoặc tăng `MAX_LOADED_MODELS` |
| Disk đầy | Quá nhiều models | `.\scripts\manage-models.ps1 remove <model>` |
| Container restart loop | Healthcheck fail | `docker compose logs ollama` |
| LAN không truy cập được | Firewall block | Mở port trong Windows Firewall |

### Docker logs

```powershell
# Xem log real-time
docker compose logs -f ollama

# Xem 50 dòng cuối
docker compose logs --tail=50 ollama
```
