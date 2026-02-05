---
name: lessons export
description: 导出 lessons 经验库到 zip 文件，方便迁移到其他机器
usage: /lessons export [output_path]
arguments:
  - name: output_path
    description: 导出 zip 文件的路径（可选，默认为桌面）
    required: false
---

# Lessons Export - 导出经验库

## 执行步骤

1. **确认导出路径**
   - 如果用户指定了 `output_path`，使用该路径
   - 否则默认导出到 `~/Desktop/lessons_export_<timestamp>.zip`

2. **执行导出脚本**

```bash
python ~/.claude/skills/lessons/scripts/export_lessons.py [output_path]
```

3. **验证导出结果**
   - 检查 zip 文件是否创建成功
   - 显示包含的文件数量和总大小

4. **提示用户**
   - 告知导出文件位置
   - 说明如何在另一台机器上导入：`/lessons import <zip_path>`

## 导出内容

导出的 zip 包含 `~/.claude/lessons/` 目录下的所有内容：
- `_index.md` - 主索引
- `global/` - 全局通用经验
- `cocos-creator/` - Cocos Creator 经验
- `rpg-framework/` - RPG 框架经验
- `projects/` - 项目特定经验

## 注意事项

- 导出不包含 skill 本身，只包含经验数据
- 目标机器需要先安装 lessons skill 才能使用导入功能
