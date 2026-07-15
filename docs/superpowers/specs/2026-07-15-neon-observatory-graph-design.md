# Neon Observatory 图谱设计

## 目标

将 AI-Brain 的 Obsidian 图谱设计为深色科幻数据观测站，同时保持节点文字、主题分组和连接方向清晰。

## 视觉系统

- 背景：深海军蓝与低亮度径向光晕，不使用纯黑。
- 纹理：极轻的工程网格和扫描线，仅用于空间感。
- MOC：金色；LinkTech：青绿；AI RAG：紫色；Security：红色；Design：粉色；Codex：电光蓝。
- 默认节点：蓝灰色；焦点节点：近白色；连线：低亮度蓝灰；高亮连线与箭头：青色。
- 字体：优先系统等宽字体，不加载网络字体。

## 可用性约束

- CSS 只作用于全局图谱和局部图谱。
- 不使用持续闪烁、Glitch 位移或高频动画。
- 扫描线不接收鼠标事件，且在“减少动态效果”模式下关闭过渡。
- 颜色组继续由属性查询控制，CSS 不覆盖分组颜色。
- 图谱使用更明显的节点、较细连线和更大的排斥力，减少拥挤。

## 实现位置

- 真实 Vault 配置：`/Users/yuanzhe/Knowledge/.obsidian/graph.json`
- CSS snippet：`/Users/yuanzhe/Knowledge/.obsidian/snippets/ai-brain-neon-observatory.css`
- 启用配置：`/Users/yuanzhe/Knowledge/.obsidian/appearance.json`

## 验收

- 外层 Vault 的图谱配置包含六个主题颜色组。
- snippet 被 appearance 配置启用。
- CSS 括号配对，无网络字体或持续动画。
- 重载 Obsidian 后，全局图谱呈现深蓝背景、网格、扫描线和霓虹主题节点。
