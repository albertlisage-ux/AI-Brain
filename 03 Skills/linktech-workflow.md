---
type: skill
topics: [linktech]
status: active
aliases: [LinkTech Workflow, LinkTech Skill]
project:
  - "[[02 Projects/LinkTech-hydraulic/linktech-project|LinkTech]]"
---

# LinkTech 工作流

**来源**: `~/.codex/worktrees/102d/LinkTech-hydraulic/.roo/skills/linktec/SKILL.md`  
**用途**: 开始 LinkTech 开发任务前的操作规则、命令与文档路由。项目身份和仓库结构以 [[02 Projects/LinkTech-hydraulic/linktech-project|项目主页]] 为准。

## 当前规则

- 活动产品详情模板：`hydraulich/templates/product-page-template-industrial-v3.php`
- 已移除旧的 `--industrial` 生成器标志
- 先更新源模板，再重新生成受影响的产品页
- 保持文档和技能文件中不含真实密码、SMTP 凭证、token 和私服密钥
- 前端 UI 改版前先读 [[linktec-frontend-taste|前端 Taste 规则]]

## 常用命令

```bash
php -l path/to/file.php
php hydraulich/generate_product_pages.php --dry-run
php hydraulich/generate_product_pages.php --status
php hydraulich/generate_product_pages.php --force
```

## 按任务查阅

| 需要 | 读取 |
|------|------|
| 版本历史和近期变更 | [[../07 Lessons/linktech-changelog\|CHANGELOG]] |
| 产品导航、卡片、模板、搜索、品牌 UI | [[../05 Architecture/linktech-product-system\|PRODUCT_SYSTEM]] |
| 前端视觉质量、反通用 UI 检查 | [[linktec-frontend-taste\|FRONTEND_TASTE]] |
| 部署、Webhook、产品生成操作 | [[../05 Architecture/linktech-deployment\|DEPLOYMENT]] |
| 已知错误和修复 | [[../07 Lessons/linktech-troubleshooting\|TROUBLESHOOTING]] |
| 安全策略、凭证、认证风险 | [[../06 Decisions/linktech-security\|SECURITY]] |
| 用户/管理员/工单内部细节 | [[../05 Architecture/linktech-user-system\|SKILLUSER]] |

---

**相关：** [[../02 Projects/LinkTech-hydraulic/linktech-project|← 项目主页]] · [[../03 Skills/skills-moc|Skills 索引]] · [[linktec-frontend-taste|前端 Taste 规则]]
