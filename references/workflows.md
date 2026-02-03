# Lessons 工作流详解

## § init

首次初始化：全量分析项目，提取经验。

### 流程

```
1. 检测项目技术栈
   ├── 扫描 package.json, tsconfig.json, settings/
   └── 生成 tech_stack 标签

2. 全量代码分析
   ├── 扫描 // NOTE: // HACK: // FIXME: 注释
   ├── 识别异常处理模式
   └── 识别工具类/基类

3. Git 历史分析
   ├── fix: commits → 踩坑记录候选
   ├── refactor: commits → 决策记录候选
   └── 同文件多次修改 → 重点踩坑

4. 项目文档提取
   ├── CLAUDE.md "已知陷阱" 章节
   └── README "常见问题" 章节

5. 汇总去重分级
   └── 每条分配层级 L1/L2/L3

6. 用户确认
   └── 可调整分类、修改内容、跳过

7. 写入
   ├── 创建 ~/.claude/lessons/ 结构（如不存在）
   ├── 写入经验文件
   ├── 更新 _index.md
   └── 创建项目 .lessons.json
```

### 技术栈检测规则

| 特征文件 | 技术栈标签 |
|----------|------------|
| `tsconfig.json` | typescript |
| `settings/cc.config.json` | cocos-creator |
| `assets/scripts/rpg/` | rpg-framework |
| `package.json` 含 react | react |
| `Cargo.toml` | rust |

### 输出示例

```markdown
## 发现的经验候选

### 踩坑 (5 条)

| # | 层级 | 标题 | 来源 | 操作 |
|---|------|------|------|------|
| 1 | L2 | XTween easing 名称必须完整拼写 | CLAUDE.md | [添加] [跳过] [编辑] |
| 2 | L2 | 禁止直接编辑 .prefab 文件 | CLAUDE.md | [添加] [跳过] [编辑] |
| ... |

### 决策 (2 条)
...

请确认要添加的经验，或输入编号编辑内容。
```

---

## § check

合规检查：扫描代码，发现违反经验库的问题。

### 流程

```
1. 加载经验
   └── 根据项目 tech_stack 加载匹配分类

2. 构建检测规则
   └── 从 pitfall 文件提取 detection_pattern

3. 扫描代码
   ├── 对每个规则执行 Grep
   └── 排除 exceptions 中的例外

4. 生成报告
   ├── ❌ 问题：违反经验库
   └── 💡 建议：可优化项

5. 处理选择
   ├── 自动修复 → AI 改代码
   ├── 标记例外 → 写入 exceptions
   └── 跳过 → 本次忽略
```

### 报告格式

```markdown
## 合规检查报告

### ❌ 问题 (2)

**CC-P001: XTween easing 名称错误**
- 文件: src/views/GameView.ts:42
- 问题: 使用了 `sineInOut`
- 正确: 应使用 `sinusoidalInOut`
- [修复] [标记例外] [跳过]

### 💡 建议 (1)

**CC-PAT001: 可使用 NodePool 优化**
- 文件: src/managers/BulletManager.ts
- 发现频繁 instantiate/destroy
- [应用模式] [跳过]
```

---

## § update

增量更新：分析新 commits 提取经验。

### 流程

```
1. 检查初始化
   └── 无 .lessons.json → 提示执行 init

2. 确定范围
   └── last_review_commit..HEAD

3. 分析 commits
   ├── fix: → 踩坑候选
   ├── refactor: → 决策候选
   └── feat: 复杂功能 → 模式候选

4. 呈现 + 确认

5. 更新
   ├── 写入新经验
   ├── 更新 _index.md
   └── 更新 last_review_commit
```

### 输出示例

```markdown
## 增量分析

分析范围: c076fe9..HEAD (5 commits)

### 发现的经验候选

| # | 类型 | 标题 | commit | 操作 |
|---|------|------|--------|------|
| 1 | 踩坑 | Vec3 normalize 需要判断零向量 | fix: 修复移动崩溃 | [添加] [跳过] |
| 2 | 决策 | 使用对象池管理弹丸 | refactor: 优化弹丸性能 | [添加] [跳过] |

请确认要添加的经验。
```

---

## § read

读取与当前项目相关的所有经验。

### 流程

```
1. 读取 .lessons.json 获取 tech_stack

2. 加载相关分类的 _overview.md
   ├── global/_overview.md (L1)
   ├── cocos-creator/_overview.md (L2, if in tech_stack)
   ├── rpg-framework/_overview.md (L2, if in tech_stack)
   └── projects/<name>/_overview.md (L3)

3. 格式化输出
```

### 输出格式

```markdown
## 项目相关经验

### L1: 通用 (3 条)
- G-P001: TypeScript 类型断言不安全...
- G-PAT001: 圆形均匀分布算法...

### L2: Cocos Creator (5 条)
- CC-P001: XTween easing 名称...
- CC-P002: 禁止直接编辑 .prefab...
- CC-D001: 动画系统选型...

### L2: RPG Framework (2 条)
- RPG-P001: 角色创建需先设置阵营...
- RPG-D001: 技能冷却统一管理...

### L3: 本项目 (1 条)
- SSDTHLY-P001: 特殊数值配置...

详情: /lessons search <关键词>
```

---

## § add

手动添加一条经验。

### 交互流程

```
1. 选择类型
   - [P] 踩坑 (刚解决的问题)
   - [D] 决策 (刚做的技术选择)
   - [PAT] 模式 (可复用的代码模式)

2. 选择层级
   - [1] L1 通用
   - [2] L2 框架级 (选择具体框架)
   - [3] L3 项目特定

3. 填写内容
   └── 根据类型加载对应模板

4. 确认 + 写入
```

### 自动建议

解决问题后，AI 应主动建议：

```markdown
💡 刚解决的问题可以记录到经验库：
   /lessons add
```
