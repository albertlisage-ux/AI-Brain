# System: OpenAI Docs Skill

**来源**: `~/.codex/skills/.system/openai-docs/`  
**用途**: OpenAI 产品与 API 文档查询、Codex 自身知识、模型选择与升级

## 信息来源优先级

1. **Codex 手册** — 通过 `scripts/fetch-codex-manual.mjs` 获取
2. **Docs MCP** — `mcp__openaiDeveloperDocs__search_openai_docs` / `fetch_openai_doc`
3. **OpenAPI Spec** — `mcp__openaiDeveloperDocs__get_openapi_spec`
4. **官方网页回退** — 仅限 `developers.openai.com` 域名

## OpenAI 产品快照

| 产品 | 说明 |
|------|------|
| Apps SDK | 为 ChatGPT 构建应用（Web Component UI + MCP Server） |
| Responses API | 统一端点，支持有状态、多模态、工具使用的 AI 交互 |
| Chat Completions API | 从消息列表生成模型回复 |
| Codex | OpenAI 的编码代理 |
| gpt-oss | 开源权重推理模型（Apache 2.0） |
| Realtime API | 低延迟语音对话 |
| Agents SDK | 构建代理应用的工具包 |

## Codex 知识源地图

当涉及 Codex 配置/扩展/操作/故障排除时：

| 场景 | 推荐途径 |
|------|---------|
| 一次性任务约束 | Prompt / 线程上下文 |
| 仓库持久约定 | `AGENTS.md` |
| 项目 Codex 设置 | `.codex/config.toml` |
| 全局默认 | 全局配置 / 全局指引 |
| 可复用工作流 | Skill |
| 可安装扩展包 | Plugin |
| 实时外部数据 | MCP Server / App Connector |
| 定时任务 | Automation |
| 生命周期强制 | Hook |

---

**相关：** [[03 Skills/codex|← 返回 Skills 索引]] · [[system-skill-creator-skill|Skill Creator]] · [[system-plugin-creator-skill|Plugin Creator]] · [[../05 Architecture/codex-system-architecture|系统架构]]
