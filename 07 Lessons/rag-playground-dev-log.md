# RAG Playground 开发日志

> 记录 AI-Brain RAG 系统 Playground 前端的开发与迭代

## 2026-07-12：多会话聊天 + localStorage 持久化

### 变更内容

在 `playground.html` 中实现了完整的**多会话聊天系统**：

- **`sessions[]` 数组**：替代原来的单 `chatHistory` 结构，支持多个独立对话
- **`localStorage` 持久化**：每次操作（发送消息、切换对话、删除等）后自动保存，刷新页面后恢复所有对话
- **侧边栏对话列表**：显示所有历史对话，默认展开最近 3 条，可点击展开/收起
- **对话操作**：点击切换对话、✕ 删除、导出（带自动删除）、新建对话
- **滚动位置保存**：切换对话时记住当前滚动位置

### 关键函数

| 函数 | 说明 |
|------|------|
| `createSession()` | 创建新对话，自增 ID `s1`, `s2`, ... |
| `renderSession(session)` | 渲染指定对话的消息到聊天区 |
| `renderHistory()` | 渲染侧边栏对话列表 |
| `switchSession(id)` | 切换当前对话，保存滚动位置 |
| `initChat()` | 从 `localStorage` 恢复或创建新对话 |
| `saveSessions()` | 保存整个 `sessions` 数组到 `localStorage` |

### 数据格式

```javascript
session = {
  id: 's1',                    // 自增 ID
  title: '新对话 1',           // 自动命名（首条消息前 30 字）
  messages: [                  // 消息数组
    { role: 'user', content: '问题' },
    { role: 'assistant', content: '回答文本', html: '<渲染后的 HTML>', _mid: 1 }
  ],
  createdAt: 1712345678901,    // 创建时间戳
  scrollPos: 0,                // 滚动位置（切换时保存）
}
```

### Debug 记录

- `exportChat()` 出现重复定义（第 522 行和第 600 行），后者覆盖前者导致 `chatHistory` 未定义错误
- 旧版 `sendQuestion` 代码残留片段（第 741-786 行）导致 JS 解析失败，所有函数无法定义
- `viewRaw()` 引用已废弃的 `chatHistory` 变量，已删除

### 修复要点

- ✅ 删除重复的 `exportChat()`，保留带自动删除功能的新版
- ✅ 删除残留的旧版 `sendQuestion` 代码片段
- ✅ 删除引用废弃变量的 `viewRaw()` 函数
- ✅ 验证 JS 括号平衡，确保无语法错误
- ✅ 验证侧边栏对话可点击切换

## 相关文档

- [[../03 Skills/ai-rag-setup-guide|AI RAG 配置指南]]
- [[../05 Architecture/codex-system-architecture|Codex 系统架构]]
