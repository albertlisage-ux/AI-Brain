# 安全工具决策记录

> 2026-07-12 导入

**相关 Skills：** [[../03 Skills/security-best-practices-skill|Security Best Practices]] · [[../03 Skills/security-ownership-map-skill|Security Ownership Map]] · [[../03 Skills/security-threat-model-skill|Security Threat Model]]

## 已安装的三种安全 Skill

### 1. Security Best Practices
- **用途**: 代码层面的安全最佳实践审查
- **适用**: 开发过程中被动发现漏洞 + 安全报告生成
- **支持语言**: Python、JavaScript/TypeScript、Go

### 2. Security Ownership Map
- **用途**: Git 历史分析 → 人员-文件所有权映射
- **适用**: 发现 orphaned 敏感代码、安全维护者、bus factor 分析
- **输出**: CSV/JSON/GraphML（支持 Neo4j/Gephi 导入）

### 3. Security Threat Model
- **用途**: 基于仓库的威胁建模
- **适用**: AppSec 级别的威胁分析，枚举信任边界、攻击路径
- **方法**: 8 步工作流，从范围界定到质量检查

## 三个工具的关系

```
Security Best Practices     Security Ownership Map       Security Threat Model
    (代码级)                    (人员/组织级)              (架构级)
       ↓                           ↓                          ↓
  发现代码漏洞              发现谁拥有敏感代码           发现系统层面的威胁
  安全编码指导              计算 bus factor             枚举攻击路径
  安全报告生成              导出图分析数据               推荐缓解措施
```
