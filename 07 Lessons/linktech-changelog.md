# LinkTec 变更日志

**来源**: `~/.codex/worktrees/102d/LinkTech-hydraulic/.roo/skills/linktec/CHANGELOG.md`  
**用途**: 项目版本历史和改版记录

## v4.0 — 2026-07-06 — Taste 引导的 Skill 清理

| 变更 | 说明 |
|------|------|
| 前端 Taste 指南 | 新增 `FRONTEND_TASTE.md` |
| 路由更新 | `SKILL.md` 现在将视觉工作路由到 Taste 指南 |
| 历史清理 | 移除过期的凭据和历史操作细节 |
| 生成安全 | 显式保留 `generate_trigger.php` 和现有生成工作流 |

## v3.9 — 2026-06-04 — 仪表盘活动标签和邮件发送者修复

| 变更 | 说明 |
|------|------|
| 仪表盘活动红esign | 分离的 Tickets 和 Login History 标签页 |
| `?tab=profile` 支持 | 仪表盘支持从页头/分类进入的 profile 深度链接 |
| 工单查询修复 | 使用 `WHERE user_id = ? OR email = ?` 匹配预登录工单 |
| SMTP 发送者名称 | 强制为 `HydraTec Support` |
| Brevo 发送者头 | 添加 `X-SIB-Sender` 保持显示名称一致性 |

文件: `users/dashboard.php`, `config/mail.php`, `hydraulich/config/mail.php`

## v3.8 — 2026-06-01 — `ticket_api.php` 500 错误修复

| 关键修复 | 说明 |
|---------|------|
| 根因 | `config/mail.php` 解析错误导致所有 `ticket_api.php` 操作失败 |
| 延迟加载 | `mail.php` 仅在 `handleReplyTicket()` 内加载 |
| 优雅回退 | 回复保存可跳过邮件发送成功 |
| 错误处理增强 | `catch (Exception)` → `catch (Throwable)` |
| 诊断脚本 | 新增 `adminmanager/diagnose_ticket_api.php` |

## v3.7 — 2026-05-30 — 自动触发和 Web 面板系统

| 变更 | 说明 |
|------|------|
| 控制面板 | `generate_trigger.php` 含 Generate/Upload/Delete 标签页 |
| 上传标签 | 浏览器拖拽上传到 `products/` |
| Webhook | `webhook.php` 接收 GitHub push 事件 |
| 诊断工具 | `diag.php`, `fix_permissions.php`, `fix_permissions.sh` |
| 生成器清理 | 源产品/分类消失时清理孤立页面 |

**生产流程**: `git push → GitHub webhook → webhook.php → git pull → generate --force`

## v3.5 — 2026-05-16 — 图片 URL 双路径修复和移动端响应式

| 变更 | 说明 |
|------|------|
| 根因 | 模板在完整 URL 前又拼接了路径前缀 |
| 修复 | 移除产品图片 `src` 属性的前缀拼接 |
| 移动端 | 添加单列布局 |
| Swiper v11 | 添加 `.swiper` class 兼容 |

## v3.4 — 2026-05-15 — 产品搜索和占位符修复

| 变更 | 说明 |
|------|------|
| 产品搜索 | 分类页添加按名称/描述的客户端搜索 |
| 硬编码修复 | "Pump" 标签在所有分类页中替换 |
| 模板占位符 | 添加 `{CATEGORY_NAME}` 和 `{category_name}` |

## v3.3–3.1 — 2026-05-13 — 品牌一致性清理

- Footer CSS 修复（`<style>` 移出 `<script>`）
- 品牌描述简化、SagePi 品牌移除
- 导航图标统一为 `fa-cogs`，蓝/青渐变
- `--industrial` 标志移除，v3 模板变为默认

## v3.0 — 2026-05-13 — 工业模板合并

- 旧标准产品模板从活跃生成路径移除
- `product-page-template-industrial-v3.php` 成为默认
- 修复了乱字符、重复读取、防护缺失等问题
- `HyraTec` 错别字修复为 `HydraTec`

---

**相关：** [[../../02 Projects/LinkTech-hydraulic/_index|← 项目主页]] · [[linktech-troubleshooting|故障排查手册]] · [[../../06 Decisions/linktech-security|安全策略]]
