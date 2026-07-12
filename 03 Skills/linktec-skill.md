# HydraTec/LinkTec Skill

**来源**: `~/.codex/worktrees/102d/LinkTech-hydraulic/.roo/skills/linktec/SKILL.md`  
**用途**: 工业液压门户项目指南 — PHP LAMP 站点、产品页面生成器、客户用户系统、管理工单系统

## 项目身份

- **品牌**: HydraTec / LinkTec
- **生产域名**: `https://www.eurohydraulicparts.com/`
- **技术栈**: PHP 7.4+, MySQL/MariaDB, Apache/LAMP, Tailwind CSS via CDN, Vanilla JS
- **前端库**: Swiper.js, Chart.js, Font Awesome

## 仓库映射

| 路径 | 用途 |
|------|------|
| `hydraulich/` | 主站、产品系统、支持页、生成器、资源、语言文件 |
| `hydraulich/products/` | 产品源文件夹树 |
| `hydraulich/productsPages/` | 分类页和生成的产品页 |
| `hydraulich/templates/` | 产品/分类生成模板 |
| `hydraulich/docus/` | 详细技术文档和报告 |
| `users/` | 客户登录、注册、仪表盘、个人资料、工单视图 |
| `adminmanager/` | 管理员登录、工单管理、仪表盘、诊断、用户管理 |
| `config/` | 共享数据库、邮件、安全、管理、语言配置 |
| `phpmyadmin/` | 轻量数据库管理工具 |

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

## 参考文档映射

| 需要 | 读取 |
|------|------|
| 版本历史和近期变更 | [[../../07 Lessons/linktech-changelog\|CHANGELOG]] |
| 产品导航、卡片、模板、搜索、品牌 UI | [[../../05 Architecture/linktech-product-system\|PRODUCT_SYSTEM]] |
| 前端视觉质量、反通用 UI 检查 | [[linktec-frontend-taste\|FRONTEND_TASTE]] |
| 部署、Webhook、产品生成操作 | [[../../05 Architecture/linktech-deployment\|DEPLOYMENT]] |
| 已知错误和修复 | [[../../07 Lessons/linktech-troubleshooting\|TROUBLESHOOTING]] |
| 安全策略、凭证、认证风险 | [[../../06 Decisions/linktech-security\|SECURITY]] |
| 用户/管理员/工单内部细节 | [[../../05 Architecture/linktech-user-system\|SKILLUSER]] |

---

**相关：** [[../02 Projects/LinkTech-hydraulic/linktec|← 项目主页]] · [[../03 Skills/codex|Skills 索引]] · [[linktec-frontend-taste|前端 Taste 规则]]
