# System: Image Generation Skill

**来源**: `~/.codex/skills/.system/imagegen/`  
**用途**: AI 图像生成与编辑（照片、插画、纹理、精灵图、原型图等）

## 两种模式

### 默认内置工具模式（首选）
- 使用内置 `image_gen` 工具
- 无需 `OPENAI_API_KEY`
- 支持生成、编辑、透明背景（通过 chroma-key 后处理）

### CLI 回退模式
- 使用 `scripts/image_gen.py` CLI
- 需要 `OPENAI_API_KEY`
- 支持 `generate`、`edit`、`generate-batch` 子命令
- 仅当用户明确要求时使用

## 透明背景处理

1. 先用内置工具生成带 chroma-key 背景的图
2. 使用 `scripts/remove_chroma_key.py` 本地移除背景
3. 复杂情况需使用 CLI 的 `gpt-image-1.5 --background transparent`

## 保存路径策略

| 场景 | 保存位置 |
|------|---------|
| 用户指定路径 | 移动/复制到指定位置 |
| 项目资产 | 移动到工作区内 |
| 预览/头脑风暴 | 保留在 `$CODEX_HOME/generated_images/` |
| 不覆盖已有文件 | 创建版本号文件如 `hero-v2.png` |

## 决策树

1. **意图**: 新生成还是编辑已有图片？
2. **执行策略**: 单个资产还是批量生成？
   - 批量 = 多次调用内置工具 或 CLI `generate-batch`

## 参考资源

- `references/prompting.md` — 提示词指南
- `references/sample-prompts.md` — 示例提示词
- `references/cli.md` — CLI 模式文档
- `references/image-api.md` — 图像 API 文档

---

**相关：** [[codex|← 返回 Skills 索引]] · [[screenshot-skill|Screenshot]] · [[pdf-skill|PDF]] · [[system-openai-docs-skill|OpenAI Docs]]
