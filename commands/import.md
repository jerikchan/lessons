---
name: lessons import
description: 从 zip 文件导入 lessons 经验库
usage: /lessons import <zip_path>
arguments:
  - name: zip_path
    description: 要导入的 zip 文件路径
    required: true
---

# Lessons Import - 导入经验库

## 执行步骤

1. **验证输入**
   - 确认 `zip_path` 参数已提供
   - 检查 zip 文件是否存在

2. **检查现有数据**
   - 如果 `~/.claude/lessons/` 已存在数据，询问用户处理方式：
     - **merge** (合并): 保留现有内容，只添加新的经验
     - **overwrite** (覆盖): 完全替换现有内容
     - **backup** (备份后覆盖): 先备份现有内容，再导入新内容

3. **执行导入脚本**

```bash
python ~/.claude/skills/lessons/scripts/import_lessons.py <zip_path> [--mode merge|overwrite|backup]
```

4. **验证导入结果**
   - 检查目录结构是否完整
   - 显示导入的经验数量

5. **重建索引（如果需要）**
   - 如果使用 merge 模式，可能需要更新 `_index.md`

## 导入模式说明

| 模式 | 行为 |
|------|------|
| `merge` | 保留现有文件，只添加 zip 中不存在的文件 |
| `overwrite` | 删除现有内容，完全使用 zip 中的内容 |
| `backup` | 备份现有内容到 `lessons_backup_<timestamp>.zip`，然后覆盖 |

## 注意事项

- 导入前建议先执行 `/lessons export` 备份当前数据
- merge 模式下，同名文件不会被覆盖
- 导入后建议执行 `/lessons status` 确认数据完整性
