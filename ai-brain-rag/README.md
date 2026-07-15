# AI-Brain RAG

本目录包含为 AI-Brain Vault 提供语义搜索和问答能力的本地服务。这里仅保留开发者快速启动信息；完整架构、API、MCP、维护和排障说明见 [AI RAG 系统配置指南](../03%20Skills/ai-rag-setup-guide.md)。

## 组件

| 组件 | 作用 |
|---|---|
| Qdrant | 保存 Markdown 分块的向量索引 |
| Indexer | 扫描 Vault、切片并生成嵌入 |
| RAG API | 提供搜索、问答、健康和统计接口 |
| MCP Server | 向 Codex 与编辑器暴露知识工具 |
| Playground | 在浏览器中测试检索和多会话问答 |

## 快速启动

```bash
cd ai-brain-rag
docker compose --env-file .env.local up -d
bash run-indexer-host.sh
curl http://localhost:8000/health
```

密钥只写入被 Git 忽略的 `.env.local`，不要写入 README、笔记或示例配置。

## 开发入口

- API：`http://localhost:8000`
- MCP：`http://localhost:8100`
- Qdrant：`http://localhost:6333/dashboard`
- Playground：直接打开 `playground.html`

日常操作、请求示例和故障处理统一维护在完整配置指南中，避免两份文档发生漂移。
