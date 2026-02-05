---
name: lessons
description: |
  跨项目开发经验积累系统 - 记录踩坑、决策和可复用模式。

  触发场景:
  (1) /lessons init - 首次初始化：分析项目代码 + Git 历史，提取经验
  (2) /lessons check - 合规检查：扫描代码，发现违反经验库的问题
  (3) /lessons update - 增量更新：分析新 commits 提取经验
  (4) /lessons read - 读取与当前项目相关的所有经验
  (5) /lessons search <关键词> - 跨项目搜索经验
  (6) /lessons status - 查看经验库统计和项目状态
  (7) /lessons add - 手动添加一条经验
  (8) /lessons export [path] - 导出经验库到 zip 文件
  (9) /lessons import <zip_path> - 从 zip 文件导入经验库

  关键词: lessons, 经验, 踩坑, pitfall, 决策, decision, ADR, 模式, pattern, 跨项目, 导出, 导入, export, import
---

# Lessons - 跨项目经验积累系统

## 存储位置

```
~/.claude/lessons/
├── _index.md                    # 主索引 + 统计
├── global/                      # L1: 技术栈通用 (TypeScript, Git)
├── cocos-creator/               # L2: 引擎级 (Cocos Creator)
├── rpg-framework/               # L2: 框架级 (RPG Framework)
└── projects/<project>/          # L3: 项目特定
```

## 命令路由

| 命令 | 动作 |
|------|------|
| `/lessons init` | 读取 [workflows.md](references/workflows.md) § init |
| `/lessons check` | 读取 [workflows.md](references/workflows.md) § check |
| `/lessons update` | 读取 [workflows.md](references/workflows.md) § update |
| `/lessons read` | 加载相关经验到上下文 |
| `/lessons search <kw>` | Grep 搜索 `~/.claude/lessons/` |
| `/lessons status` | 读取 `_index.md` + 项目 `.lessons.json` |
| `/lessons add` | 交互式添加经验 |
| `/lessons export [path]` | 读取 [commands/export.md](commands/export.md) |
| `/lessons import <zip>` | 读取 [commands/import.md](commands/import.md) |

## 经验分层

| 层级 | 目录 | 适用范围 |
|------|------|----------|
| L1 | `global/` | 所有项目 (TypeScript, Git, 算法) |
| L2 | `cocos-creator/`, `rpg-framework/` | 使用该框架的项目 |
| L3 | `projects/<name>/` | 仅该项目 |

## 经验类型

| 类型 | ID 后缀 | 模板 |
|------|---------|------|
| Pitfall (踩坑) | `-P###` | [pitfall.md](references/templates/pitfall.md) |
| Decision (决策) | `-D###` | [decision.md](references/templates/decision.md) |
| Pattern (模式) | `-PAT###` | [pattern.md](references/templates/pattern.md) |

## ID 前缀

| 前缀 | 分类 |
|------|------|
| `G-` | global |
| `CC-` | cocos-creator |
| `RPG-` | rpg-framework |
| `<PROJECT>-` | 项目特定 |

## 项目状态文件

每个项目维护 `.lessons.json`：

```json
{
  "initialized_at": "2026-02-03T10:30:00Z",
  "tech_stack": ["typescript", "cocos-creator", "rpg-framework"],
  "last_review_commit": "c076fe9",
  "exceptions": []
}
```

## 快速操作

### 读取经验

```bash
# 读取当前项目相关经验
/lessons read

# 搜索特定关键词
/lessons search easing
```

### 添加经验

```bash
# 交互式添加
/lessons add

# 从当前问题添加
# (解决问题后 AI 自动建议)
```

### 检查代码

```bash
# 扫描违规代码
/lessons check
```
