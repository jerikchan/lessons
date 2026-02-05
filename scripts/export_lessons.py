#!/usr/bin/env python3
"""
Export lessons library to a zip file.
Usage: python export_lessons.py [output_path]
"""

import os
import sys
import zipfile
from pathlib import Path
from datetime import datetime

LESSONS_ROOT = Path.home() / ".claude" / "lessons"


def get_default_output_path():
    """Get default output path (Desktop or home directory)."""
    desktop = Path.home() / "Desktop"
    if desktop.exists():
        base_dir = desktop
    else:
        base_dir = Path.home()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return base_dir / f"lessons_export_{timestamp}.zip"


def export_lessons(output_path: Path) -> dict:
    """
    Export lessons directory to a zip file.
    Returns statistics about the export.
    """
    if not LESSONS_ROOT.exists():
        raise FileNotFoundError(f"Lessons directory not found: {LESSONS_ROOT}")

    stats = {
        "files": 0,
        "directories": 0,
        "total_size": 0,
        "categories": set()
    }

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(LESSONS_ROOT):
            root_path = Path(root)
            rel_root = root_path.relative_to(LESSONS_ROOT)

            # Track categories (top-level directories)
            if rel_root != Path('.') and rel_root.parent == Path('.'):
                stats["categories"].add(str(rel_root))

            for file in files:
                file_path = root_path / file
                arcname = str(rel_root / file) if rel_root != Path('.') else file

                zipf.write(file_path, arcname)
                stats["files"] += 1
                stats["total_size"] += file_path.stat().st_size

            stats["directories"] += len(dirs)

    stats["categories"] = sorted(stats["categories"])
    stats["output_path"] = str(output_path)
    stats["output_size"] = output_path.stat().st_size

    return stats


def format_size(size_bytes: int) -> str:
    """Format bytes to human readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def main():
    # Parse arguments
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        print("\nArguments:")
        print("  output_path  Path for the output zip file (optional)")
        print("\nExamples:")
        print("  python export_lessons.py")
        print("  python export_lessons.py ~/my_lessons.zip")
        print("  python export_lessons.py C:/backup/lessons.zip")
        return 0

    # Get output path
    if len(sys.argv) > 1:
        output_path = Path(sys.argv[1]).expanduser().resolve()
        # Add .zip extension if not present
        if not output_path.suffix.lower() == '.zip':
            output_path = output_path.with_suffix('.zip')
    else:
        output_path = get_default_output_path()

    print(f"Exporting lessons from: {LESSONS_ROOT}")
    print(f"Output file: {output_path}")
    print()

    try:
        stats = export_lessons(output_path)

        print("Export completed successfully!")
        print()
        print("Statistics:")
        print(f"  Files exported: {stats['files']}")
        print(f"  Directories: {stats['directories']}")
        print(f"  Original size: {format_size(stats['total_size'])}")
        print(f"  Compressed size: {format_size(stats['output_size'])}")
        print(f"  Categories: {', '.join(stats['categories']) or 'None'}")
        print()
        print(f"Output: {stats['output_path']}")
        print()
        print("To import on another machine:")
        print(f"  /lessons import <path_to_zip>")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Run '/lessons init' first to create the lessons library.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
