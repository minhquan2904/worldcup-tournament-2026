# Docker — Cheat Sheet & Lưu Ý Quan Trọng

> Tổng hợp các khái niệm, lệnh, và bẫy thường gặp khi dùng Docker + Docker Compose.

---

## 1. Data Persistence — Dữ liệu sống ở đâu?

Đây là phần **quan trọng nhất** và hay gây nhầm lẫn nhất.

### 3 cách lưu data trong Docker

```
┌─────────────────────────────────────────────────────────────┐
│ Container filesystem (ephemeral)                            │
│ → Mất khi container bị xoá (docker rm)                     │
│ → KHÔNG mất khi container stop/restart                     │
├─────────────────────────────────────────────────────────────┤
│ Named Volume (Docker quản lý)                               │
│ → docker volume create my-data                              │
│ → Lưu tại /var/lib/docker/volumes/my-data/_data            │
│ → Persist qua container lifecycle                           │
│ → Mất khi: docker volume rm HOẶC docker compose down -v    │
├─────────────────────────────────────────────────────────────┤
│ Bind Mount (bạn quản lý)                                    │
│ → Map thẳng folder trên host vào container                  │
│ → Data luôn nằm trên máy bạn, Docker không quản lý         │
│ → KHÔNG BAO GIỜ mất vì Docker commands                     │
└─────────────────────────────────────────────────────────────┘
```

### So sánh chi tiết

| | Container FS | Named Volume | Bind Mount |
|---|---|---|---|
| **Khai báo** | Mặc định | `volumes:` section | `./path:/container/path` |
| `docker stop` | ✅ Giữ | ✅ Giữ | ✅ Giữ |
| `docker rm` (xoá container) | ❌ **Mất** | ✅ Giữ | ✅ Giữ |
| `docker compose down` | ❌ Mất | ✅ **Giữ** | ✅ Giữ |
| `docker compose down -v` | ❌ Mất | ❌ **Mất** | ✅ **Giữ** |
| `docker system prune -a` | ❌ Mất | ⚠️ Tuỳ flag | ✅ Giữ |
| `docker volume prune` | — | ❌ **Mất** (nếu orphan) | ✅ Giữ |
| Xem file trên host | `docker exec` | `docker exec` hoặc tìm path | Mở folder bình thường |
| Backup | Khó | `docker cp` hoặc mount temp | Copy folder |
| Dùng khi | Data tạm, cache | DB data, model weights | Config, source code, logs |

### ⚠️ Bẫy thường gặp

```bash
# ❌ NGUY HIỂM: -v xoá TẤT CẢ named volumes của compose project
docker compose down -v

# ✅ AN TOÀN: chỉ stop + xoá containers, giữ volumes
docker compose down

# ✅ AN TOÀN: chỉ stop, giữ containers + volumes
docker compose stop
```

```bash
# ❌ NGUY HIỂM: xoá orphan volumes (volumes không gắn container nào)
docker volume prune

# ⚠️ CỰC KỲ NGUY HIỂM: xoá mọi thứ không dùng
docker system prune -a --volumes
```

---

## 2. Docker Compose — Các lệnh hay dùng

### Lifecycle

```bash
# Build image + start containers
docker compose up --build -d

# Start (không rebuild)
docker compose up -d

# Stop (giữ containers)
docker compose stop

# Stop + xoá containers (GIỮ volumes)
docker compose down

# Stop + xoá containers + xoá volumes (CẨN THẬN!)
docker compose down -v

# Restart 1 service
docker compose restart mcp-test-agent

# Xem logs
docker compose logs -f mcp-test-agent
docker compose logs --tail=50 mcp-test-agent
```

### Debug

```bash
# Exec vào container
docker compose exec mcp-test-agent bash
docker compose exec mcp-test-agent sh    # nếu image không có bash

# Chạy 1 lệnh trong container
docker compose exec mcp-test-agent python -c "print('hello')"

# Xem trạng thái
docker compose ps

# Xem resource usage
docker stats
```

### Build

```bash
# Build lại image (khi sửa code)
docker compose build

# Build không dùng cache (khi thay đổi requirements.txt)
docker compose build --no-cache

# Build + start
docker compose up --build -d
```

---

## 3. Volumes — Quản lý

```bash
# Liệt kê tất cả volumes
docker volume ls

# Xem chi tiết volume (đường dẫn trên host)
docker volume inspect <volume_name>

# Xoá 1 volume cụ thể
docker volume rm <volume_name>

# Xoá volumes orphan (KHÔNG gắn container nào)
docker volume prune

# Backup volume sang tar
docker run --rm -v <volume_name>:/data -v $(pwd):/backup \
  alpine tar czf /backup/volume-backup.tar.gz -C /data .
```

---

## 4. Networking

### Container gọi container cùng compose

```yaml
# Dùng service name làm hostname
services:
  web:
    environment:
      - DB_HOST=database    # ← service name
  database:
    image: postgres
```

### Container gọi host machine

```yaml
services:
  app:
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      - API_URL=http://host.docker.internal:8080
```

### Container gọi container KHÁC compose project

```bash
# Cách 1: Dùng host.docker.internal (đơn giản)
# Container A (compose A) → http://host.docker.internal:PORT → Container B (compose B)

# Cách 2: Shared network (phức tạp hơn)
docker network create shared-net
# Thêm `networks: shared-net` vào cả 2 compose files
```

---

## 5. Image Management

```bash
# Liệt kê images
docker images

# Xoá image không dùng
docker image prune

# Xoá TẤT CẢ images không dùng (kể cả dangling)
docker image prune -a

# Xem disk usage
docker system df
```

---

## 6. Dockerfile — Best Practices

### Layer caching (quan trọng cho build speed)

```dockerfile
# ✅ ĐÚNG: Copy requirements trước, install, rồi mới copy code
COPY requirements.txt .
RUN pip install -r requirements.txt    # Layer này cache nếu requirements không đổi
COPY . .                                # Layer này rebuild khi code đổi

# ❌ SAI: Copy tất cả rồi install → mỗi lần sửa code đều phải pip install lại
COPY . .
RUN pip install -r requirements.txt
```

### .dockerignore

Tạo file `.dockerignore` để tránh copy rác vào image:

```
__pycache__/
*.pyc
.git/
.env
*.md
.vscode/
specs/
```

### Multi-stage build (giảm image size)

```dockerfile
# Stage 1: Build
FROM python:3.12 AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime (nhỏ hơn)
FROM python:3.12-slim
COPY --from=builder /root/.local /root/.local
COPY . .
```

---

## 7. Lưu ý cho dự án Test Agent

| Thành phần | Cách lưu | Lý do |
|------------|---------|-------|
| **Ollama models** (~2-5GB) | Named volume `ollama-models` | Docker quản lý, tự cleanup |
| **Specs uploads** | Bind mount `./specs` | Xem/debug được, không mất |
| **Config** | Bind mount `./config.yaml:ro` | Sửa nhanh, read-only |
| **Skills** | Bind mount `./skills:ro` | Sửa templates nhanh |
| **Python code** | Baked in image (COPY) | Ổn định, version controlled |
| **Python code (dev)** | Bind mount (uncomment) | Dev nhanh, không rebuild |

### Quy trình an toàn

```bash
# Ngày thường: sửa config/skills → restart
docker compose restart mcp-test-agent

# Sửa Python code → rebuild
docker compose up --build -d

# Update image base / deps → rebuild no-cache
docker compose build --no-cache && docker compose up -d

# Cleanup disk khi đầy
docker system df              # xem dung lượng
docker image prune            # xoá images cũ
docker builder prune          # xoá build cache
# TUYỆT ĐỐI KHÔNG chạy: docker system prune -a --volumes
```
