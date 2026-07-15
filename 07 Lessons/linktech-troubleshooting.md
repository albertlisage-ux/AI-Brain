---
type: lesson
topics: [linktech, troubleshooting]
status: active
project:
  - "[[02 Projects/LinkTech-hydraulic/linktech-project|LinkTech]]"
---

# LinkTec 故障排查手册

**来源**: `~/.codex/worktrees/102d/LinkTech-hydraulic/.roo/skills/linktec/TROUBLESHOOTING.md`  
**用途**: 已知错误模式的首选排查来源

## 常见错误速查

| 症状 | 可能原因 | 修复 |
|------|---------|------|
| 数据库连接失败 | DB 凭据错误或 MySQL 服务不可用 | 验证凭据、服务状态和 PDO MySQL 扩展 |
| 登录无跳转 | 已在发送 header 前输出内容或 session 问题 | 检查 header() 前的空白输出、session 启动顺序 |
| 登录成功但仪表盘缺工单 | 工单 `user_id = NULL` | 查询使用 `WHERE user_id = ? OR email = ?` |
| `ticket_api.php` 500 空响应 | 顶层 include 或 mail 配置解析错误 | mail 仅在回复路径内加载，catch Throwable |
| 产品图片缺失 | 文件夹名错误、URL 双路径 | 直接使用 helper 返回的 URL，不拼接前缀 |
| 产品图灰/黑背景 | CSS 给 `.product-image` 加了深色渐变 | `background: none !important; padding: 0 !important;` |
| 移动端画廊空白 | Swiper 初始化/CSS 不匹配 | 添加 `.swiper` 兼容类和回退 CSS |
| 多语言文本缺失 | 缺少语言文件或 key | 确认 `en.php/de.php/fr.php` 都有同一 key |
| 分类页显示错误产品 | `$categoryName` 硬编码为其他分类 | 修正 `$categoryName`，从模板重新生成 |
| 生成页内容陈旧 | 模板更新但页面未重新生成 | 运行 generator status/dry-run 后再 force |
| Webhook 无反应 | URL 错误、服务器无法 pull、权限问题 | 检查 GitHub delivery 日志和服务器 git 状态 |

## 诊断工具

```bash
# PHP 语法检查
php -l path/to/file.php

# 产品生成器检查
php hydraulich/generate_product_pages.php --dry-run
php hydraulich/generate_product_pages.php --status
```

**数据库/用户诊断**:
- `adminmanager/test_table_connection.php`
- `adminmanager/test_api_integration.php`
- `adminmanager/diagnose_users_api.php`
- `users/check_schema.php`, `users/fix_schema.php`

**工单诊断**:
- `adminmanager/diagnose_ticket_api.php`
- `adminmanager/test_ticket_api.php`
- `users/diagnose_login.php`
- `hydraulich/support/diagnose_ticket.php`

**服务器/生成器诊断**:
- `hydraulich/diag.php`
- `hydraulich/fix_permissions.php`
- `hydraulich/generation_log.txt`

## 保留的高价值调试笔记

### 仪表盘活动和工单可见性

- 预登录提交的工单 `user_id` 可能为 NULL → 查询需同时匹配 email
- 正确的查询模式：`WHERE user_id = ? OR email = ?`
- 先初始化 `$pdo = null` 再进入 try/catch
- 保留 `?tab=profile` 深度链接

### `ticket_api.php` 500 模式

- 根因通常是 PHP 解析/致命错误发生在 JSON 输出前
- 保持非必要 include 在文件顶层之外
- 加载 mail 配置仅在回复处理内
- catch `Throwable` 而非 `Exception`
- 确保 `ticket_replies` 表在获取回复前存在

调试路径：
1. 检查浏览器响应体是否为空
2. `php -l config/mail.php` 和 `php -l adminmanager/ticket_api.php`
3. 运行 `adminmanager/diagnose_ticket_api.php`
4. 确认非回复的 API 操作不依赖 mail 配置

### 图片 URL 模式

- 共享 helper 可能返回完整 URL，模板不应再拼接路径
- 正确：`<img src="<?= htmlspecialchars($image) ?>" alt="">`
- 错误：`$imageUrlPrefix . 'Hero/' . $filename` — 导致双重路径

### 生成器清理

- 生成器可在源产品/分类文件夹消失时移除孤立的生成页面
- 清理前：检查源文件夹 → dry-run → 确认生成路径 → 备份

---

**相关：** [[../02 Projects/LinkTech-hydraulic/linktech-project|← 项目主页]] · [[linktech-changelog|变更日志]] · [[../05 Architecture/linktech-user-system|用户系统]] · [[../05 Architecture/linktech-deployment|部署运维]]
