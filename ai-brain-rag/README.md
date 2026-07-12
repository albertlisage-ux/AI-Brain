# AI-Brain RAG System

> 本地 RAG 系统，为 Obsidian Vault 提供语义搜索和 AI 问答能力

## 架构

```
Obsidian Markdown         Indexer (定时扫描)
      │                         │
      └─────► Chunker ──► Embedding ──► Qdrant
                                              │
                                    ┌─────────┼─────────┐
                                    ▼         ▼         ▼
                                 RAG API   MCP Server  Codex/VS Code
                                    │
                                    ▼
                              DeepSeek API
```

## 启动

```bash
cd ai-brain-rag

# 1. 配置 .env（DeepSeek API Key）
cp .env .env.local
# 编辑 .env.local 填入 DEEPSEEK_API_KEY

# 2. 启动所有服务
docker compose --env-file .env.local up -d

# 3. 查看日志
docker compose logs -f
```

## 服务

| 服务 | 端口 | 说明 |
|------|------|------|
| Qdrant | 6333 / 6334 | 向量数据库 |
| RAG API | 8000 | HTTP 查询接口 |
| MCP Server | 8100 | MCP 协议接口 |

## API 使用

```bash
# 搜索（不调用 DeepSeek）
curl http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"question": "Kafka 重试策略", "top_k": 5}'

# 问答（检索 + DeepSeek）
curl http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Kafka 重试策略是什么？", "top_k": 5}'

# 按文件夹过滤
curl http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"question": "前端设计", "top_k": 3, "filters": {"folder": "03 Skills"}}'

# 健康检查
curl http://localhost:8000/health

# 统计
curl http://localhost:8000/stats
```

## MCP 配置（Codex / VS Code）

在 VS Code 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "ai-brain": {
      "url": "http://localhost:8100"
    }
  }
}
```

可用工具：

| 工具 | 说明 |
|------|------|
| `search_knowledge` | 语义搜索知识库 |
| `read_note` | 读取完整笔记 |
| `list_notes` | 列出笔记 |
| `get_project_context` | 获取项目上下文 |
| `get_skill` | 获取 Skill 文档 |

## 索引器

自动每 30 秒扫描 vault，仅处理新增或修改的文件。状态保存在 `data/` 目录。
