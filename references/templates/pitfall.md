# Pitfall (踩坑) 模板

## 文件命名

`<ID>.md` 例如: `CC-P001-xtween-easing.md`

## 模板

```markdown
# [ID]: [标题]

**分类**: [category]
**严重程度**: 🔴 高 / 🟡 中 / 🟢 低
**首次发现**: YYYY-MM-DD
**来源项目**: [project]

## 错误现象

[描述错误表现]

## 根因分析

[解释为什么会犯这个错误]

## 正确做法

\`\`\`typescript
// 正确示例
\`\`\`

## 经验提炼

> [一句话总结]

## 检测规则

\`\`\`yaml
detection:
  type: regex | ast | manual
  pattern: "[正则表达式]"
  files: "*.ts"
  exclude: ["node_modules", "dist"]
\`\`\`
```

## 示例

```markdown
# CC-P001: XTween easing 名称必须完整拼写

**分类**: cocos-creator
**严重程度**: 🟡 中
**首次发现**: 2026-01-15
**来源项目**: ssd_thly

## 错误现象

使用 `sineInOut` 作为 easing 名称，运行时报错 "Unknown easing function"。

## 根因分析

XTween 使用完整的数学术语命名，而非缩写。开发者习惯其他库的缩写形式。

## 正确做法

\`\`\`typescript
// ❌ 错误
XTween.to(node, 1, { alpha: 0 }, { easing: "sineInOut" });

// ✅ 正确
XTween.to(node, 1, { alpha: 0 }, { easing: "sinusoidalInOut" });
\`\`\`

## 经验提炼

> XTween easing 名称是完整拼写，不是缩写。

## 检测规则

\`\`\`yaml
detection:
  type: regex
  pattern: "easing:\\s*[\"']sine(In|Out|InOut)[\"']"
  files: "*.ts"
  suggestion: "使用 sinusoidal 替代 sine"
\`\`\`
```
