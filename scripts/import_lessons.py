#!/usr/bin/env python3
"""
Import lessons library from a zip file.
Usage: python import_lessons.py <zip_path> [--mode merge|overwrite|backup]
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

LESSONS_ROOT = Path.home() / ".claude" / "lessons"


def backup_existing(backup_dir: Path = None) -> Path:
    """Create a backup of existing lessons directory."""
    if not LESSONS_ROOT.exists():
        return None

    if backup_dir is None:
        desktop = Path.home() / "Desktop"
        if desktop.exists():
            backup_dir = desktop
        else:
            backup_dir = Path.home()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"lessons_backup_{timestamp}.zip"

    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(LESSONS_ROOT):
            root_path = Path(root)
            rel_root = root_path.relative_to(LESSONS_ROOT)

            for file in files:
                file_path = root_path / file
                arcname = str(rel_root / file) if rel_root != Path('.') else file
                zipf.write(file_path, arcname)

    return backup_path


def validate_zip(zip_path: Path) -> dict:
    """Validate the zip file and return info about its contents."""
    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file not found: {zip_path}")

    if not zipfile.is_zipfile(zip_path):
        raise ValueError(f"Invalid zip file: {zip_path}")

    info = {
        "files": 0,
        "has_index": False,
        "categories": set()
    }

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for name in zipf.namelist():
            info["files"] += 1

            if name == "_index.md":
                info["has_index"] = True

            # Extract top-level directory names
            parts = name.split('/')
            if len(parts) > 1 and parts[0]:
                info["categories"].add(parts[0])

    info["categories"] = sorted(info["categories"])
    return info


def import_lessons(zip_path: Path, mode: str = "merge") -> dict:
    """
    Import lessons from a zip file.

    Modes:
    - merge: Keep existing files, only add new ones
    - overwrite: Replace all existing content
    - backup: Backup existing content, then overwrite

    Returns statistics about the import.
    """
    stats = {
        "files_imported": 0,
        "files_skipped": 0,
        "backup_path": None,
        "mode": mode
    }

    # Handle backup mode
    if mode == "backup" and LESSONS_ROOT.exists():
        stats["backup_path"] = str(backup_existing())
        mode = "overwrite"  # After backup, proceed with overwrite

    # Handle overwrite mode
    if mode == "overwrite" and LESSONS_ROOT.exists():
        shutil.rmtree(LESSONS_ROOT)

    # Ensure lessons root exists
    LESSONS_ROOT.mkdir(parents=True, exist_ok=True)

    # Extract files
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for member in zipf.namelist():
            # Skip directory entries
            if member.endswith('/'):
                continue

            target_path = LESSONS_ROOT / member

            # In merge mode, skip existing files
            if mode == "merge" and target_path.exists():
                stats["files_skipped"] += 1
                continue

            # Ensure parent directory exists
            target_path.parent.mkdir(parents=True, exist_ok=True)

            # Extract file
            with zipf.open(member) as src, open(target_path, 'wb') as dst:
                dst.write(src.read())

            stats["files_imported"] += 1

    return stats


def main():
    # Parse arguments
    if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) < 2:
        print(__doc__)
        print("\nArguments:")
        print("  zip_path     Path to the zip file to import (required)")
        print("  --mode       Import mode: merge, overwrite, or backup (default: merge)")
        print()
        print("Modes:")
        print("  merge      Keep existing files, only add new ones")
        print("  overwrite  Replace all existing content")
        print("  backup     Backup existing content first, then overwrite")
        print()
        print("Examples:")
        print("  python import_lessons.py ~/lessons_export.zip")
        print("  python import_lessons.py ~/lessons.zip --mode overwrite")
        print("  python import_lessons.py ~/lessons.zip --mode backup")
        return 0 if "--help" in sys.argv or "-h" in sys.argv else 1

    # Get zip path
    zip_path = Path(sys.argv[1]).expanduser().resolve()

    # Get mode
    mode = "merge"
    if "--mode" in sys.argv:
        mode_idx = sys.argv.index("--mode")
        if mode_idx + 1 < len(sys.argv):
            mode = sys.argv[mode_idx + 1].lower()
            if mode not in ("merge", "overwrite", "backup"):
                print(f"Error: Invalid mode '{mode}'. Use merge, overwrite, or backup.")
                return 1

    print(f"Importing lessons from: {zip_path}")
    print(f"Target directory: {LESSONS_ROOT}")
    print(f"Mode: {mode}")
    print()

    try:
        # Validate zip file
        info = validate_zip(zip_path)
        print(f"Zip file contains {info['files']} files")
        print(f"Categories: {', '.join(info['categories']) or 'None'}")

        if not info["has_index"]:
            print("Warning: Zip file does not contain _index.md")
        print()

        # Check existing data
        if LESSONS_ROOT.exists() and any(LESSONS_ROOT.iterdir()):
            print("Existing lessons directory detected.")
            if mode == "merge":
                print("Mode 'merge': Existing files will be preserved.")
            elif mode == "overwrite":
                print("Mode 'overwrite': Existing files will be DELETED.")
            elif mode == "backup":
                print("Mode 'backup': Existing files will be backed up first.")
            print()

        # Perform import
        stats = import_lessons(zip_path, mode)

        print("Import completed successfully!")
        print()
        print("Statistics:")
        print(f"  Files imported: {stats['files_imported']}")
        if stats['files_skipped'] > 0:
            print(f"  Files skipped (already exist): {stats['files_skipped']}")
        if stats['backup_path']:
            print(f"  Backup created: {stats['backup_path']}")
        print()
        print("Next steps:")
        print("  /lessons status  - View imported lessons")
        print("  /lessons read    - Load lessons into context")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
