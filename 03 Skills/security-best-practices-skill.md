# Security Best Practices Skill

**来源**: `~/.codex/skills/security-best-practices/`  
**用途**: 语言/框架安全最佳实践审查、安全报告、安全编码

## 使用场景

- 用户明确请求安全最佳实践指导、安全审查/报告、安全编码帮助
- 仅支持：Python、JavaScript/TypeScript、Go
- 不用于：一般代码审查、调试、非安全任务

## 工作流程

1. **识别** — 确定项目使用的语言和框架（前后端都要）
2. **加载参考** — 从 `references/` 目录加载对应语言/框架的安全文档
3. **三种模式**：
   - **主动模式** — 编写新代码时自动遵循安全最佳实践
   - **被动模式** — 工作时发现严重漏洞并提示
   - **报告模式** — 用户要求安全报告时，生成完整报告

## 报告格式

- 文件：`security_best_practices_report.md`
- 包含：执行摘要、按严重程度分级的发现、影响说明、代码行号
- 修复：一次修复一个发现，避免破坏项目功能

## 通用安全建议

| 建议 | 说明 |
|------|------|
| ✅ 使用 UUID4 替代自增 ID | 防止资源枚举和信息泄露 |
| ❌ 不报告缺少 TLS（开发环境） | 开发环境通常由代理处理 TLS |
| ❌ 不推荐 HSTS | 可能导致重大故障和用户锁定 |
| ❌ `secure` cookie 仅在 TLS 下启用 | 非 TLS 下设置会破坏应用 |

## 覆盖规则

- 项目可能有特殊需求需要绕开安全实践
- 绕开时建议记录到项目文档中说明原因

---

**相关：** [[_index|← 返回 Skills 索引]] · [[security-ownership-map-skill|Security Ownership Map]] · [[security-threat-model-skill|Security Threat Model]] · [[../06 Decisions/security-tools-decision-log|安全工具决策]]
