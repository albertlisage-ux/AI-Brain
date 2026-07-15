# PDF Skill

**来源**: `~/.codex/skills/pdf/`  
**用途**: 读取、创建、审查 PDF 文件，关注布局和渲染质量

## 核心工作流

1. **视觉优先** — 使用 `pdftoppm` 将 PDF 渲染为 PNG 后检查
2. **生成** — 使用 `reportlab` 创建 PDF
3. **文本提取** — 使用 `pdfplumber` 或 `pypdf`

## 依赖

| 工具 | 安装方式 |
|------|---------|
| reportlab | `pip install reportlab` |
| pdfplumber | `pip install pdfplumber` |
| pypdf | `pip install pypdf` |
| poppler (pdftoppm) | `brew install poppler` (macOS) |

## 输出约定

- 临时文件 → `tmp/pdfs/`
- 最终产物 → `output/pdf/`
- 文件名稳定且具描述性

## 质量检查项

- [x] 排版一致（字体、间距、边距、层级）
- [x] 无渲染问题（文字裁剪、重叠、表格断裂、乱码）
- [x] 图表/表格/图片清晰对齐
- [x] 仅使用 ASCII 连字符，避免 Unicode 破折号
- [x] 引用可读，无工具 token 占位符

---

**相关：** [[03 Skills/codex|← 返回 Skills 索引]] · [[../05 Architecture/codex-system-architecture|系统架构]] · [[system-imagegen-skill|ImageGen]]
