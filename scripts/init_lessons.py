#!/usr/bin/env python3
"""
Initialize the global lessons library structure.
Creates the directory hierarchy and index files.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

LESSONS_ROOT = Path.home() / ".claude" / "lessons"

INDEX_TEMPLATE = """# Global Lessons Library

> Cross-project development experience | Last updated: {date}

## Statistics

| Level | Category | Pitfalls | Decisions | Patterns | Total |
|-------|----------|----------|-----------|----------|-------|
| L1 | global | 0 | 0 | 0 | 0 |
| L2 | cocos-creator | 0 | 0 | 0 | 0 |
| L2 | rpg-framework | 0 | 0 | 0 | 0 |

## Category Index

| Category | Description | Applicable Projects | Entry |
|----------|-------------|---------------------|-------|
| global | TypeScript, Git, General Programming | All | [Link](global/_overview.md) |
| cocos-creator | Cocos Creator Engine | Cocos projects | [Link](cocos-creator/_overview.md) |
| rpg-framework | RPG Framework | RPG projects | [Link](rpg-framework/_overview.md) |

## Recent Updates

| Date | Type | Category | Title | Source |
|------|------|----------|-------|--------|
| - | - | - | No entries yet | - |
"""

CATEGORY_TEMPLATE = """# {name} Lessons

> Applicable to: {scope} | Entries: 0

## Pitfalls Quick Reference

| ID | Title | Error | Correct | Source |
|----|-------|-------|---------|--------|
| - | - | - | - | - |

## Decisions Quick Reference

| ID | Title | Choice | Reason | Source |
|----|-------|--------|--------|--------|
| - | - | - | - | - |

## Patterns Quick Reference

| ID | Pattern | Scenario | Details |
|----|---------|----------|---------|
| - | - | - | - |
"""

CATEGORIES = {
    "global": {
        "name": "Global (L1)",
        "scope": "All projects (TypeScript, Git, algorithms)"
    },
    "cocos-creator": {
        "name": "Cocos Creator (L2)",
        "scope": "Cocos Creator 3.x projects"
    },
    "rpg-framework": {
        "name": "RPG Framework (L2)",
        "scope": "Projects using RPG framework"
    }
}


def create_directory_structure():
    """Create the lessons directory structure."""
    print(f"Creating lessons library at: {LESSONS_ROOT}")

    # Create root directory
    LESSONS_ROOT.mkdir(parents=True, exist_ok=True)

    # Create main index
    index_path = LESSONS_ROOT / "_index.md"
    if not index_path.exists():
        index_path.write_text(
            INDEX_TEMPLATE.format(date=datetime.now().strftime("%Y-%m-%d")),
            encoding="utf-8"
        )
        print(f"  Created: _index.md")
    else:
        print(f"  Exists: _index.md")

    # Create category directories
    for cat_id, cat_info in CATEGORIES.items():
        cat_dir = LESSONS_ROOT / cat_id
        cat_dir.mkdir(exist_ok=True)

        # Create subdirectories
        for subdir in ["pitfalls", "decisions", "patterns"]:
            (cat_dir / subdir).mkdir(exist_ok=True)

        # Create overview file
        overview_path = cat_dir / "_overview.md"
        if not overview_path.exists():
            overview_path.write_text(
                CATEGORY_TEMPLATE.format(**cat_info),
                encoding="utf-8"
            )
            print(f"  Created: {cat_id}/_overview.md")
        else:
            print(f"  Exists: {cat_id}/_overview.md")

    # Create projects directory
    projects_dir = LESSONS_ROOT / "projects"
    projects_dir.mkdir(exist_ok=True)
    print(f"  Created: projects/")

    print("\nLessons library initialized successfully!")
    print(f"Location: {LESSONS_ROOT}")


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        print("\nUsage: python init_lessons.py")
        return

    create_directory_structure()


if __name__ == "__main__":
    main()
