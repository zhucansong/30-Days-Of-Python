"""Rename files by removing a specific prefix.

This script scans the given directory for files whose names start with the
specified prefix and renames them by stripping that prefix. It is intended to
help remove the prefix ``AQT 3034-2010 化工企业工艺安全管理实施导则 - `` from files
in the directory ``/Users/zhucansong/Qsync/工作/6 个人资料与学习/职业卫生标准库/04 其他``.
"""

from argparse import ArgumentParser
from pathlib import Path

PREFIX = "AQT 3034-2010 化工企业工艺安全管理实施导则 - "


def rename_files(target_dir: Path, prefix: str = PREFIX) -> int:
    """Rename files in ``target_dir`` that start with ``prefix``.

    Returns the number of files renamed.
    """

    renamed = 0
    for path in target_dir.iterdir():
        if not path.is_file():
            continue

        name = path.name
        if not name.startswith(prefix):
            continue

        new_name = name[len(prefix) :]
        if not new_name:
            # Avoid creating an empty filename.
            continue

        destination = path.with_name(new_name)
        if destination.exists():
            print(f"Skipping '{path.name}' because '{destination.name}' already exists.")
            continue

        path.rename(destination)
        print(f"Renamed '{path.name}' -> '{destination.name}'")
        renamed += 1

    return renamed


def main() -> None:
    parser = ArgumentParser(description="Remove a specific prefix from filenames in a directory.")
    parser.add_argument(
        "directory",
        type=Path,
        help=(
            "Path to the directory containing files to rename. "
            "Example: '/Users/zhucansong/Qsync/工作/6 个人资料与学习/职业卫生标准库/04 其他'"
        ),
    )
    parser.add_argument(
        "--prefix",
        default=PREFIX,
        help="Filename prefix to remove (default matches the AQT guidance prefix).",
    )

    args = parser.parse_args()
    directory: Path = args.directory.expanduser()

    if not directory.is_dir():
        raise SystemExit(f"Directory not found: {directory}")

    count = rename_files(directory, args.prefix)
    print(f"Completed: renamed {count} file(s).")


if __name__ == "__main__":
    main()
