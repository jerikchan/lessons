# Pattern (模式) 模板

## 文件命名

`<ID>.md` 例如: `G-PAT001-circle-distribution.md`

## 模板

```markdown
# [模式名称]

**分类**: [category]
**适用场景**: [描述]
**验证项目**: [project]

## 问题

[这个模式解决什么问题]

## 反模式

\`\`\`typescript
// ❌ 常见错误做法
\`\`\`

## 正确模式

\`\`\`typescript
// ✅ 推荐做法
\`\`\`

## 原理解释

[为什么这样做是对的]

## 变体

[模式的变种用法]

## 相关经验

- [链接到相关的踩坑/决策]
```

## 示例

```markdown
# G-PAT001: 圆形均匀分布算法

**分类**: global
**适用场景**: 需要在圆形/环形区域均匀分布点的场景
**验证项目**: ssd_thly

## 问题

在圆形区域内均匀随机放置物品时，直接使用 `random() * radius` 会导致中心区域密度过高。

## 反模式

\`\`\`typescript
// ❌ 错误：中心会更密集
function randomInCircle(radius: number): Vec2 {
  const angle = Math.random() * Math.PI * 2;
  const r = Math.random() * radius;  // 错误！
  return new Vec2(Math.cos(angle) * r, Math.sin(angle) * r);
}
\`\`\`

## 正确模式

\`\`\`typescript
// ✅ 正确：使用 sqrt 校正
function randomInCircle(radius: number): Vec2 {
  const angle = Math.random() * Math.PI * 2;
  const r = Math.sqrt(Math.random()) * radius;  // sqrt 校正
  return new Vec2(Math.cos(angle) * r, Math.sin(angle) * r);
}
\`\`\`

## 原理解释

圆的面积与半径平方成正比 (A = πr²)。如果 r 均匀分布，外圈面积大但点少，中心面积小但点多，导致密度不均。

使用 `sqrt(random())` 使得 r² 均匀分布，从而在各个半径的环带上点密度相同。

## 变体

\`\`\`typescript
// 环形分布 (内径 minR，外径 maxR)
function randomInRing(minR: number, maxR: number): Vec2 {
  const angle = Math.random() * Math.PI * 2;
  const r = Math.sqrt(Math.random() * (maxR * maxR - minR * minR) + minR * minR);
  return new Vec2(Math.cos(angle) * r, Math.sin(angle) * r);
}

// 圆周上均匀分布 N 个点
function distributeOnCircle(n: number, radius: number): Vec2[] {
  return Array.from({ length: n }, (_, i) => {
    const angle = (i / n) * Math.PI * 2;
    return new Vec2(Math.cos(angle) * radius, Math.sin(angle) * radius);
  });
}
\`\`\`

## 相关经验

- 适用于：散落物品、粒子初始位置、敌人刷新点
```
