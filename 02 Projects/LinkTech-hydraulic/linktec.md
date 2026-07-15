---
type: project
topics: [linktech, hydraulic]
status: active
---

# LinkTech-hydraulic 项目

> 源自 `~/.codex/worktrees/102d/LinkTech-hydraulic/.roo/skills/linktec/`
> 导入日期：2026-07-12
> **AI-Brain 远程**: `git@github.com:albertlisage-ux/AI-Brain.git`

## Git 关系

```mermaid
graph LR
    AB[AI-Brain 仓库] -->|git submodule| LH[LinkTech-hydraulic/code/]
    LH -->|指向| REMOTE[git@github.com:albertlisage-ux/LinkTech-hydraulic.git]
    
    subgraph "本目录（笔记）"
        INDEX[linktec.md]
        SKILL[03 Skills/ 引用]
        ARCH[05 Architecture/ 引用]
    end
    
    INDEX -.->|笔记| LH
    SKILL -.->|记录 Skill| LH
    ARCH -.->|记录架构| LH
```

## 项目身份

| 属性 | 值 |
|------|-----|
| 品牌 | HydraTec / LinkTec |
| 线上域名 | `https://www.eurohydraulicparts.com/` |
| 技术栈 | PHP 7.4+, MySQL/MariaDB, Apache/LAMP |
| 前端 | Tailwind CSS (CDN), Vanilla JS, Swiper.js, Chart.js, Font Awesome |
| 核心功能 | 产品门户、产品页面生成器、客户账户、支持工单、管理后台、多语言、浏览器端生成工具 |

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

## 项目知识路径

| 分类 | 文件 | 说明 |
|------|------|------|
| 📋 项目能力 | [[03 Skills/linktec-skill\|Skill 入口]] | 执行项目前应遵循的仓库映射、规则和命令 |
| 🔐 用户系统 | [[../../05 Architecture/linktech-user-system\|用户与工单系统]] | 认证流、注册流、工单 API 详细技术文档 |
| 🏗 产品系统 | [[../../05 Architecture/linktech-product-system\|产品系统架构]] | 导航、卡片、模板、品牌 UI 规则 |
| 🎨 前端设计 | [[../../03 Skills/linktec-frontend-taste\|前端 Taste 规则]] | 工业门户前端品质检查 |
| 🚀 部署运维 | [[../../05 Architecture/linktech-deployment\|部署与运维]] | 部署、Webhook、产品生成操作 |
| 🔒 安全策略 | [[../../06 Decisions/linktech-security\|安全与凭证策略]] | 认证、CSRF、Session、凭证规则 |
| 📜 变更历史 | [[../../07 Lessons/linktech-changelog\|变更日志]] | 版本历史与改版记录 |
| 🔧 故障排查 | [[../../07 Lessons/linktech-troubleshooting\|故障排查手册]] | 常见错误与修复方案 |

## Git Submodule

此项目的实际代码仓库作为 Git Submodule 关联：

```bash
# 克隆 AI-Brain 后初始化子模块
git clone git@github.com:albertlisage-ux/AI-Brain.git
cd AI-Brain
git submodule update --init --recursive

# 或克隆时同时拉取子模块
git clone --recursive git@github.com:albertlisage-ux/AI-Brain.git
```

| 信息 | 值 |
|------|-----|
| AI-Brain 远程 | `git@github.com:albertlisage-ux/AI-Brain.git` |
| 子模块路径 | `code/` |
| 子模块远程 | `git@github.com:albertlisage-ux/LinkTech-hydraulic.git` |
| 关系 | AI-Brain 父仓库 → Submodule `code/` → LinkTech-hydraulic 代码 |

> 📌 笔记文件（`linktec.md` 等）在 AI-Brain 仓库中管理，`code/` 子模块指向实际项目代码的特定 commit。

## 跨项目知识

- [[../../codex|返回 AI-Brain 总入口]] — 切换到其他主题或知识类型。
- [[03 Skills/codex|Skills MOC]] — 查找可复用到其他项目的工作流。
- [[05 Architecture/codex-system-architecture|Codex 系统架构]] — 理解项目使用的 Codex 工具环境。
- [[06 Decisions/codex-config-decisions|Codex 配置决策]] — 追溯工具环境的配置取舍。

## 常用命令

```bash
# PHP 语法检查
php -l path/to/file.php

# 产品页面生成
php hydraulich/generate_product_pages.php --dry-run
php hydraulich/generate_product_pages.php --status
php hydraulich/generate_product_pages.php --force
```
