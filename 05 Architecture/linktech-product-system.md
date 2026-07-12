# LinkTec 产品系统架构

**来源**: `~/.codex/worktrees/102d/LinkTech-hydraulic/.roo/skills/linktec/PRODUCT_SYSTEM.md`  
**用途**: 产品导航、分类页、产品详情页、产品卡片、搜索、品牌 UI 规则

## 目录驱动系统

```
产品源文件夹: hydraulich/products/{CATEGORY}/{PRODUCT}/
生成详情页:  hydraulich/productsPages/{CATEGORY}/{PRODUCT}/{PRODUCT}.php
分类页:       hydraulich/productsPages/{CATEGORY}/{CATEGORY}.php
```

## 关键文件

| 文件 | 用途 |
|------|------|
| `productsPages/product_navigation.php` | 导航帮助函数和图片扫描 |
| `productsPages/products.php` | 主产品导航页 |
| `productsPages/product-details.php` | 旧版通用产品详情页 |
| `productsPages/get_categories.php` | 分类 API |
| `productsPages/get_products.php` | 产品 API |
| `css/product-navigation.css` | 导航样式 |
| `js/product-navigation.js` | 客户端行为 |
| `templates/category-page-template.php` | 分类页生成模板 |
| `templates/product-page-template-industrial-v3.php` | **活动产品详情模板** |

## 品牌标识

```html
<!-- 白色导航栏 -->
<div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg ...">
    <i class="fa-solid fa-cogs text-white text-lg"></i>
</div>
<span class="text-2xl font-black text-gray-900">Hydra<span class="text-blue-600">Tec</span></span>
<span class="text-xs text-gray-500 block -mt-1">Industrial Solutions</span>
```

## 产品详情模板特征

| 特征 | 说明 |
|------|------|
| Hero 区域 | 深色海军蓝/钢色工业 Hero，两列布局 |
| Hero 统计 | 件号、系列、分类、重量风格统计卡 |
| Swiper 画廊 | 键盘/触摸支持，分页/导航 |
| 概览卡片 | 按关键字自动分配图标 |
| 规格表 | 四列（Parameter/Metric/Bar/Imperial） |
| 文档标签 | Datasheet/Manual/Certificate/Software |
| 兼容型号 | 相关产品卡片/网格 |
| 图片弹窗 | 全屏、箭头导航、Esc 关闭 |
| 阅读进度条 | 固定顶部进度条 |

## 关键帮助函数

| 函数 | 用途 |
|------|------|
| `getImagesInDirectory($dir)` | 扫描图片文件 |
| `getFirstImage($dir)` | 返回第一张图片 |
| `readDescriptionFile($path)` | 读取描述文件（含拼写回退） |
| `formatProductOverview($text)` | 格式化概览卡片 |
| `parseSpecsCSV($text)` | 解析 CSV 规格表 |
| `getDocsFiles($folder)` | 按文件名分类文档 |
| `formatFileSize($bytes)` | 可读文件大小 |
| `generateBreadcrumb()` | 面包屑 HTML |

---

**相关：** [[../../02 Projects/LinkTech-hydraulic/_index|← 项目主页]] · [[../../03 Skills/linktec-frontend-taste|前端 Taste 规则]] · [[../../03 Skills/linktec-skill|Skill 入口]]
