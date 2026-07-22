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

## Codex 会话归档

会话归档由快速 Stop hook 与后台 worker 组成。hook 只把 `session_id` 和
`transcript_path` 合并写入 SQLite；静默 5 分钟后，worker 使用现有 DeepSeek
配置生成结构化笔记，并写入 `02 Projects/Codex Conversations/YYYY/MM/`。
原始 transcript 不会复制到 Vault 或 Qdrant。

在现有 `.env.local` 中保留/配置以下变量（不要把值提交到 Git）：

```text
DEEPSEEK_API_KEY
DEEPSEEK_API_BASE
DEEPSEEK_MODEL
OBSIDIAN_VAULT_PATH
```

`OBSIDIAN_VAULT` 也受支持并优先于兼容名称 `OBSIDIAN_VAULT_PATH`。可选变量包括
`CODEX_SESSIONS_ROOT`、`CONVERSATION_ARCHIVE_DB`、
`CONVERSATION_QUIET_SECONDS`、`CODEX_CAPACITY_WARNING_BYTES` 和
`CODEX_CAPACITY_GROWTH_PERCENT`。

```bash
# 安装/幂等更新 Stop hook 与两个用户 LaunchAgent
bash scripts/install-automation.sh

# 查看状态与日志
launchctl print gui/$(id -u)/com.yuanzhe.ai-brain-conversation-archive
launchctl print gui/$(id -u)/com.yuanzhe.ai-brain-indexer
tail -f data/logs/conversation-archive.error.log data/logs/indexer.error.log

# 仅卸载项目拥有的 LaunchAgent；保留 hook、状态、笔记和报告
bash scripts/uninstall-automation.sh
```

容量报告每月写入 `02 Projects/Codex Conversations/Reports/`。达到 5 GiB
或增长阈值时只显示预警；任何脚本都不会压缩、移动、修改或删除
`~/.codex/sessions`。解析器集中在 `conversation_archive/transcript.py`，以便
Codex JSONL 格式变化时单独更新。失败任务保留在 SQLite 并指数重试；修复配置或
本地服务后重载 LaunchAgent 即可恢复。
