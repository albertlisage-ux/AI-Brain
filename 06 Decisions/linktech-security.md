---
type: decision
topics: [linktech, security]
status: active
project:
  - "[[02 Projects/LinkTech-hydraulic/linktec|LinkTech]]"
---

# LinkTec 安全与凭证策略

**来源**: `~/.codex/worktrees/102d/LinkTech-hydraulic/.roo/skills/linktec/SECURITY.md`  
**用途**: 认证、会话、CSRF、诊断、邮件、数据库、上传安全规则

## 凭证规则

- ❌ 不提交真实 DB 密码、SMTP 密码、API token、Webhook secret
- ❌ 不将真实 secret 放入 Skill 文件、文档、示例、截图或故障排查片段
- ✅ 使用占位符：`DB_HOST=<host>`, `DB_PASS=<server-secret>`
- ✅ 生产 secret 存在服务器配置或环境变量中

## 认证要求

| 要求 | 实现 |
|------|------|
| 密码哈希 | `password_hash()` + `password_verify()` (bcrypt) |
| Session 固定防护 | `session_regenerate_id(true)` |
| 通用登录错误消息 | 公开/客户流程不暴露具体原因 |
| 管理员路由检查 | 使用管理员 session 检查，非客户 session 检查 |
| 工单所有权检查 | 基于 `user_id` 和/或已验证的 email 匹配 |

## CSRF 防护

所有修改性表单和 AJAX 操作应包含 CSRF token：

```php
$csrf_token = generateCSRFToken();
// 验证时使用 hash_equals()
```

**高优先级审查区域**:
- `users/login_proc.php`, `users/register_proc.php`
- `adminmanager/ticket_api.php`
- 个人资料、密码、工单回复、删除、标记、上传、生成操作

## Remember-Me Cookie

当前实现不完整 — token **未持久化到数据库**，因此 cookie 实际上不提供自动登录。

必须项（当前缺少）：
- [ ] Token 在服务端持久化（哈希存储）
- [ ] Token 有过期时间
- [ ] Token 使用后轮换
- [ ] 退出/改密码时失效
- [ ] Cookie 设置 `HttpOnly`、`Secure`、`SameSite`

## Session 与 Cookie 生产设置

- `HttpOnly` ✅
- `Secure` ✅（生产环境）
- `SameSite=Lax` 或更严格
- Session ID 登录时重新生成 ✅
- Session 退出时销毁 ✅
- 管理员 session 空闲超时

## 数据库安全

- ✅ 使用 PDO 预处理语句
- ✅ `utf8mb4`
- ✅ 捕获数据库错误并记录脱敏上下文
- ✅ 不向公共用户展示原始 DB 错误
- ❌ 避免从原始请求参数构建 SQL

## 输出与输入处理

- ✅ `htmlspecialchars()` 转义 HTML 输出
- ✅ `FILTER_VALIDATE_EMAIL` 验证邮箱
- ✅ 验证枚举字段（工单状态、紧急程度、部门等）
- ✅ 标准化文件名、限制上传目录

## 诊断工具安全

诊断脚本很有用但也有风险。需保护或限制公共访问：

- `adminmanager/diagnose_ticket_api.php`
- `adminmanager/diagnose_users_api.php`
- `users/diagnose_login.php`
- `hydraulich/diag.php`
- `hydraulich/support/diagnose_ticket.php`

诊断不得暴露：密码/token、SMTP 凭据、原始 Session ID、客户个人数据。

## 生产加固清单

1. ✅ `display_errors=Off`
2. ✅ HTTPS 强制
3. ✅ Secret 排除在 Git/文档外
4. ✅ 管理诊断受保护
5. ✅ CSRF 在修改操作上启用
6. ✅ Session 登录后重新生成
7. ✅ Cookie 安全设置
8. ✅ SQL 使用预处理语句
9. ✅ 输出转义
10. ✅ 上传路径受限

---

**相关：** [[../02 Projects/LinkTech-hydraulic/linktec|← 项目主页]] · [[../05 Architecture/linktech-user-system|用户系统]] · [[../03 Skills/security-best-practices-skill|通用安全实践]]
