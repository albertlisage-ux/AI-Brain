# LinkTec 部署与运维

**来源**: `~/.codex/worktrees/102d/LinkTech-hydraulic/.roo/skills/linktec/DEPLOYMENT.md`  
**用途**: 部署、Webhook、产品生成、浏览器控制面板、权限工作流

## 生产环境 URL

| 用途 | URL |
|------|-----|
| 主站 | `https://www.eurohydraulicparts.com/` |
| 产品导航 | `https://www.eurohydraulicparts.com/hydraulich/products.php` |
| 客户登录 | `https://www.eurohydraulicparts.com/users/login.php` |
| 管理后台 | `https://www.eurohydraulicparts.com/adminmanager/linktec-manager.php` |
| 产品生成面板 | `https://www.eurohydraulicparts.com/hydraulich/generate_trigger.php` |
| Webhook 面板 | `https://www.eurohydraulicparts.com/hydraulich/webhook.php` |

## 产品生成

```bash
# 预览将要生成的内容
php hydraulich/generate_product_pages.php --dry-run

# 查看当前状态
php hydraulich/generate_product_pages.php --status

# 强制执行生成
php hydraulich/generate_product_pages.php --force
```

**规则**:
- 不使用已删除的 `--industrial` 标志
- 活动模板: `product-page-template-industrial-v3.php`
- 源数据: `hydraulich/products/{CATEGORY}/{PRODUCT}/`
- 生成页面: `hydraulich/productsPages/{CATEGORY}/{PRODUCT}/{PRODUCT}.php`

## 源文件夹结构

```
hydraulich/products/{CATEGORY}/{PRODUCT}/
├── Hero/
│   ├── image
│   └── HeroDescription.txt
├── List/
│   ├── image
│   └── ListDescription.txt
├── Preview/
│   ├── image
│   └── PreviewDescription.txt
└── docs/
```

## GitHub Webhook 流程

```
git push → GitHub push webhook
  → https://www.eurohydraulicparts.com/hydraulich/webhook.php
  → server git pull
  → php hydraulich/generate_product_pages.php --force
  → 产品页上线
```

**Webhook 设置**:
- Payload URL: `https://www.eurohydraulicparts.com/hydraulich/webhook.php`
- Content type: `application/json`
- Events: push events only

## 浏览器控制面板

`hydraulich/generate_trigger.php` 提供浏览器端操作：

| 标签页 | 功能 |
|--------|------|
| Generate | 浏览器中运行生成和清理 |
| Upload | 上传产品文件夹到 `products/` |
| Delete | 删除源产品/分类文件夹及对应生成页面 |

## 部署检查清单

1. ✅ 确认 PHP 7.4+ 和 PDO MySQL
2. ✅ 确认 MySQL/MariaDB 连接
3. ✅ 凭据放在服务器上，不在 Git 或文档中
4. ✅ `php -l` 检查更改的 PHP 文件
5. ✅ 模板更改后先 dry-run 再 `--force`
6. ✅ 验证公共产品页和代表性详情页
7. ✅ 验证客户登录/仪表盘
8. ✅ 验证管理员工单回复流程
9. ✅ 保护诊断工具不受未认证公共访问

## 需要写权限的路径

- `hydraulich/logs/`
- `.page_generation_cache.json`
- 浏览器上传面板使用的产品上传文件夹

---

**相关：** [[../../02 Projects/LinkTech-hydraulic/linktec|← 项目主页]] · [[../../05 Architecture/linktech-user-system|用户系统]] · [[../../07 Lessons/linktech-troubleshooting|故障排查]]
