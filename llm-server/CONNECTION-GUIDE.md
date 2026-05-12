# LLM Server — Connection Guide

> Hướng dẫn kết nối đến Ollama LLM Service từ mọi nơi: local, Docker container, LAN, IDE.

---

## Trạng thái hiện tại

| Mục | Giá trị |
|-----|---------|
| Host IP (LAN) | `192.168.1.7` |
| Ollama port | `11434` |
| Docker image | `ollama/ollama:0.21.2` |
| Default model | `qwen2.5-coder:3b` |

---

## Kiến trúc kết nối

```
┌──────────────────────────────────────────────────────────┐
│ Máy host (192.168.1.7)                                   │
│                                                          │
│   ┌──────────────────────┐                               │
│   │ Docker: Ollama       │                               │
│   │ container port 11434 │──── expose ──── host:11434    │
│   └──────────────────────┘                     │         │
│                                                │         │
│   ┌──────────────────────┐                     │         │
│   │ Docker: Test Agent   │                     │         │
│   │ (port 8001)          │── host.docker ──────┘         │
│   └──────────────────────┘   .internal                   │
│                                                │         │
│   ┌──────────────────────┐                     │         │
│   │ IDE / Terminal        │── localhost:11434 ──┘         │
│   └──────────────────────┘                               │
│                                                          │
└──────────────────────────┬───────────────────────────────┘
                           │ LAN (192.168.1.x)
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────┴─────┐   ┌─────┴─────┐   ┌─────┴─────┐
    │ Máy dev A │   │ Máy dev B │   │ Máy dev C │
    │ IDE/Agent │   │ IDE/Agent │   │ IDE/Agent │
    └───────────┘   └───────────┘   └───────────┘
      192.168.1.7:11434 (Ollama)
      192.168.1.7:8001  (Test Agent MCP)
```

---

## Kết nối theo từng scenario

### 1. Từ máy host (local)

```bash
# Test Ollama
curl http://localhost:11434/api/tags

# Gọi chat
curl http://localhost:11434/api/chat -d '{
  "model": "qwen2.5-coder:3b",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": false
}'
```

**URL:** `http://localhost:11434`

---

### 2. Từ Docker container khác (cùng host)

Container trong Docker không thấy `localhost` của host. Dùng DNS đặc biệt:

**URL:** `http://host.docker.internal:11434`

```yaml
# docker-compose.yml của service cần gọi Ollama
services:
  my-app:
    environment:
      - OLLAMA_URL=http://host.docker.internal:11434
    extra_hosts:
      - "host.docker.internal:host-gateway"    # Bắt buộc trên Linux
      # Windows/Mac: Docker Desktop tự resolve, nhưng thêm cho chắc
```

> **Lưu ý:** `host.docker.internal` là DNS Docker tự tạo, resolve về IP của host machine. Trên Linux cần thêm `extra_hosts`, trên Windows/Mac Docker Desktop tự hỗ trợ.

---

### 3. Từ máy khác trong LAN

**URL:** `http://192.168.1.7:11434`

```bash
# Từ máy đồng nghiệp
curl http://192.168.1.7:11434/api/tags
```

**Yêu cầu:**
- Ollama phải set `OLLAMA_HOST=0.0.0.0` (đã config trong docker-compose)
- Windows Firewall cho phép port 11434 (xem mục Firewall bên dưới)
- Cùng subnet (192.168.1.x)

---

### 4. Từ IDE — Continue.dev (VS Code / JetBrains)

#### Cùng máy host

```json
// .continue/config.json
{
  "models": [{
    "title": "Qwen2.5-Coder (Local)",
    "provider": "ollama",
    "model": "qwen2.5-coder:3b",
    "apiBase": "http://localhost:11434"
  }]
}
```

#### Từ máy khác trong LAN

```json
{
  "models": [{
    "title": "Qwen2.5-Coder (Team Server)",
    "provider": "ollama",
    "model": "qwen2.5-coder:3b",
    "apiBase": "http://192.168.1.7:11434"
  }]
}
```

---

### 5. Từ Test Agent MCP (đã config sẵn)

```env
# mcp-test-agent/.env
LLM_BASE_URL=http://host.docker.internal:11434
```

Luồng: Test Agent container → `host.docker.internal:11434` → host → Ollama container

---

### 6. Từ Python script (local dev)

```python
import requests

response = requests.post("http://localhost:11434/api/chat", json={
    "model": "qwen2.5-coder:3b",
    "messages": [{"role": "user", "content": "Write a unit test"}],
    "stream": False,
})
print(response.json()["message"]["content"])
```

---

## Windows Firewall

Nếu máy khác trong LAN không kết nối được, mở port trên Windows Firewall:

```powershell
# Mở port 11434 (Ollama) — chạy PowerShell as Admin
New-NetFirewallRule -DisplayName "Ollama LLM" `
  -Direction Inbound -Protocol TCP -LocalPort 11434 -Action Allow

# Mở port 8001 (Test Agent MCP)
New-NetFirewallRule -DisplayName "Test Agent MCP" `
  -Direction Inbound -Protocol TCP -LocalPort 8001 -Action Allow

# Kiểm tra rules đã tạo
Get-NetFirewallRule -DisplayName "Ollama*","TestAgent*" | Format-Table
```

---

## Troubleshooting

| Vấn đề | Từ đâu | Nguyên nhân | Fix |
|--------|--------|-------------|-----|
| `Connection refused` | Local | Ollama chưa start | `cd ollama && docker compose up -d` |
| `Connection refused` | Container | Thiếu `extra_hosts` | Thêm `host.docker.internal:host-gateway` |
| `Connection refused` | LAN | Firewall block | Mở port (xem trên) |
| `Connection refused` | LAN | Ollama chỉ listen localhost | Set `OLLAMA_HOST=0.0.0.0` |
| `Model not found` | Bất kỳ | Model chưa pull | `docker exec ollama-ollama-1 ollama pull <model>` |
| Timeout / rất chậm | Bất kỳ | Model quá lớn cho GPU | Đổi model nhỏ hơn |
| `OOM killed` | Bất kỳ | Hết VRAM | Giảm model size hoặc `--num-ctx` |

---

## Health Check Script

Chạy script này để verify toàn bộ kết nối:

```bash
# 1. Ollama container running?
docker ps | grep ollama

# 2. API accessible từ host?
curl -s http://localhost:11434/api/tags | python -m json.tool

# 3. Model loaded?
curl -s http://localhost:11434/api/tags | python -c "
import sys, json
data = json.load(sys.stdin)
models = [m['name'] for m in data.get('models', [])]
print('Models:', models)
print('qwen2.5-coder:3b loaded:', any('qwen2.5-coder' in m for m in models))
"

# 4. Test inference
curl -s http://localhost:11434/api/chat -d '{
  "model": "qwen2.5-coder:3b",
  "messages": [{"role": "user", "content": "return 1+1"}],
  "stream": false
}' | python -c "import sys,json; print(json.load(sys.stdin)['message']['content'][:200])"
```

---

## Tóm tắt URL

| Từ đâu | URL Ollama | Ghi chú |
|--------|-----------|---------|
| Máy host | `http://localhost:11434` | Mặc định |
| Docker container cùng host | `http://host.docker.internal:11434` | Cần `extra_hosts` trên Linux |
| Máy LAN | `http://192.168.1.7:11434` | Cần firewall + OLLAMA_HOST=0.0.0.0 |
| Anywhere (port forward) | `http://<public_ip>:11434` | Không khuyến nghị — không có auth |
