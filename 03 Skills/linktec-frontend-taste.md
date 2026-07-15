# LinkTec Frontend Taste Rules

**来源**: `~/.codex/worktrees/102d/LinkTech-hydraulic/.roo/skills/linktec/FRONTEND_TASTE.md`  
**用途**: B2B 工业液压门户的前端设计品质指南

## 设计读取

```
B2B industrial parts portal for procurement and technical buyers,
with a restrained hydraulic/industrial visual language,
leaning toward clear product inspection, trustworthy navigation, and low-motion polish.
```

## 设计旋钮

| 旋钮 | 值 | 含义 |
|------|-----|------|
| Design Variance | 4-5 | 结构化、略工业化、非实验性 |
| Motion Intensity | 2-4 | 仅 hover/focus/reveal，无滚动劫持 |
| Visual Density | 5-7 | 产品数据可扫读且紧凑 |

## 硬性约束

- 保持 URL、分类/产品文件夹名、生成的文件路径、表单字段名不变
- 先更新源模板，再重新生成受影响页面
- 产品图片必须使用真实产品图片（Hero/List/Preview），不可用装饰性插画
- 保持 HydraTec/LinkTec 品牌，不 reintroduce SagePi

## 视觉方向

- **配色**: 白色/石板色（目录页），海军蓝/石板色（工业详情页）
- **强调色**: 蓝/青色 — HydraTec 默认强调色
- **禁止**: AI 紫色辉光、随机渐变、米色/黄铜手工艺调色板
- **排版**: 保留现有字体栈，产品名称和分类名称容易扫读
- **形状**: 统一的圆角系统，卡片仅用于真正的产品/分类实体

## 产品页规则

- Hero 区域：产品图必须在首屏可见，CTA 无需滚动
- 画廊：使用真实产品图片，`object-fit: contain`，保留键盘/触摸行为
- 规格：长规格表可接受，需分组清晰，不编造数据
- 文档：保持分类（datasheet/test report/certificate/other）

## 动效与交互

- 动效应传达状态或层级，而非装饰
- 默认使用 CSS transitions 和小 hover lift
- 尊重 `prefers-reduced-motion`
- 禁止滚动劫持、视差、无限跑马灯、磁性光标

## 文案规则

- 使用平实的工业语言，避免 "elevate"、"next-gen"、"seamless"
- 不使用 em dash，使用逗号/句号/冒号/连字符替代
- 保持多语言 key 在 `en.php`、`de.php`、`fr.php` 中完整

## 发布前检查清单

- [ ] 产品/分类导航支持空格和非 ASCII 名称
- [ ] 图片是真实产品资源，从编码 URL 加载
- [ ] Hero 适配桌面和移动端首屏
- [ ] 桌面导航保持单行，高度低于 80px
- [ ] 文本对比度在所有 CTA、表单、浮层上可读
- [ ] 移动端使用明确的一列回退布局

---

**相关：** [[linktec-skill|← Skill 入口]] · [[../02 Projects/LinkTech-hydraulic/linktec|项目主页]] · [[03 Skills/taste-skill|通用 Taste Skill]]
