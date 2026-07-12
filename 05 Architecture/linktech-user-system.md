# LinkTec 用户系统与管理员 — 技术文档

**来源**: `~/.codex/worktrees/102d/LinkTech-hydraulic/.roo/skills/linktec/SKILLUSER.md`  
**用途**: 客户用户系统和管理员支持工单系统的完整技术参考

## 系统概述

两个互联子系统：

| 子系统 | 目录 | URL 路径 | 受众 |
|--------|------|----------|------|
| 用户系统 | `users/` | `/users/` | 注册客户 |
| 管理后台 | `adminmanager/` | `/adminmanager/` | 支持人员和管理员 |

**共享数据库表**: `support_tickets`, `ticket_replies`, `users`, `user_profiles`, `user_activities`, `login_logs`

**共享配置**: `config/db.php`, `config/mail.php`, `config/security.php`

---

## 1. 用户认证系统

### 登录流程图

```
Login Page (login.php)
       │
       ▼ POST (JSON fetch API)
login_proc.php
       │
       ├──► auth_functions.php::authenticateUser()
       │       ├──► getDBConnection() → PDO
       │       ├──► SELECT ... FROM users WHERE (username=? OR email=?) AND status='active'
       │       ├──► password_verify($password, $user['password_hash'])
       │       ├──► UPDATE users SET last_login=NOW(), last_ip=? WHERE id=?
       │       ├──► logLoginAttempt() / logUserActivity()
       │       └──► getUserProfile() → LEFT JOIN user_profiles
       │
       ├──► Set $_SESSION vars
       ├──► session_regenerate_id(true)
       ├──► Optional: setcookie('remember_token', bin2hex(random_bytes(32)), 30 days)
       └──► JSON response {success, message, redirect, user}
```

### 注册流程图

```
Register Page (register.php)
       │
       ▼ POST (JSON fetch API)
register_proc.php
       │
       ├──► 客户端验证 + 服务端验证
       ├──► auth_functions.php::registerUser()
       │       ├──► validateEmail() + validatePassword()
       │       ├──► PDO Transaction
       │       ├──► INSERT INTO users
       │       ├──► INSERT INTO user_profiles
       │       ├──► logUserActivity('registration')
       │       └──► PDO::commit()
       │
       └──► Auto-login → 设置 SESSION → JSON 返回
```

## 2. 管理员工单系统

`adminmanager/ticket_api.php` 提供 AJAX 工单操作 API。

### 关键端点

| 操作 | 方法 | 说明 |
|------|------|------|
| `get_replies` | GET | 获取工单回复 |
| `handleReplyTicket` | POST | 回复工单 |
| `edit` | POST | 编辑工单/回复 |
| `mark` | POST | 标记状态 |
| `delete` | POST | 删除 |

### 已知陷阱

- `config/mail.php` 的解析错误会级联导致所有 `ticket_api.php` 操作返回 500
- 修复方案：mail 配置仅在 `handleReplyTicket()` 内部加载
- 邮件发送失败不应阻止回复保存

## 关键数据库代码

| 代码 | 用途 |
|------|------|
| PDO 1045 | 访问拒绝 — 凭证或权限问题 |
| PDO 1049 | 未知数据库 — `DB_NAME` 错误 |
| PDO 2002 | 连接拒绝 — MySQL 主机/服务/socket |

---

**相关：** [[../../02 Projects/LinkTech-hydraulic/_index|← 项目主页]] · [[linktech-deployment|部署运维]] · [[../../06 Decisions/linktech-security|安全策略]] · [[../../07 Lessons/linktech-troubleshooting|故障排查]]
