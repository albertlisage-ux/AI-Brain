# Taste Skill (Anti-Slop Frontend Skill)

**来源**: `~/.codex/skills/taste-skill/`  
**用途**: 着陆页、作品集、改版的前端设计 — 防止 AI 模板化输出

## 核心概念：三个旋钮

| 旋钮 | 范围 | 说明 | 默认值 |
|------|------|------|--------|
| `DESIGN_VARIANCE` | 1-10 | 1=完美对称, 10=艺术混乱 | 8 |
| `MOTION_INTENSITY` | 1-10 | 1=静态, 10=电影/物理 | 6 |
| `VISUAL_DENSITY` | 1-10 | 1=画廊/留白, 10=驾驶舱/密集 | 4 |

## 设计读取（先读氛围再动手）

输出一行设计判断后再写代码：
> "Reading this as: \<页面类型> for \<受众>, with a \<风格> language, leaning toward \<设计系统或审美家族>."

## 设计系统映射

| 场景 | 推荐方案 |
|------|---------|
| Microsoft / 企业 SaaS | `@fluentui/react-components` |
| Google / Material | `@material/web` |
| IBM B2B 企业分析 | `@carbon/react` |
| Shopify 应用 | Polaris React |
| Atlassian 风格 | `@atlaskit/*` |
| GitHub 风格 | `@primer/css` |
| 英国公共部门 | `govuk-frontend` |
| 美国公共部门 | `uswds` |
| 现代 React 无障碍 | `@radix-ui/themes` |
| 现代 SaaS 自有组件 | shadcn/ui |
| Tailwind 现代 SaaS | Tailwind v4 |

## 禁止的 AI 默认风格

❌ AI 紫色渐变  
❌ 居中 hero + 深色网格  
❌ 三个均等功能卡片  
❌ 通用毛玻璃  
❌ 无限循环微动效  
❌ Inter + slate-900

---

**相关：** [[03 Skills/codex|← 返回 Skills 索引]] · [[ui-ux-pro-max-skill|UI/UX Pro Max]] · [[../06 Decisions/taste-skill-design-philosophy|设计理念详解]]
