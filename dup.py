#!/usr/bin/env python3

import hashlib
from datetime import datetime
from pathlib import Path

import click


def get_sha256(filepath: Path) -> str:
    hsh = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hsh.update(chunk)
    return hsh.hexdigest()


@click.command(help="Find duplicate files in a directory")
@click.argument(
    "folder",
    default=".",
    type=click.Path(exists=True, path_type=Path, file_okay=False),
    required=True,
)
@click.option(
    "-d",
    "--delete",
    help="Delete newest/oldest",
    default="old",
    type=click.Choice(["new", "old"]),
)
@click.option(
    "-r", "--dry-run", help="Do not delete files", is_flag=True, default=False
)
@click.option(
    "-y", "--yes", help="skip delete confirmation", is_flag=True, default=False
)
def dup(folder: Path, delete: str, dry_run: bool, yes: bool):
    files = folder.glob("**/*")
    files = [f for f in files if f.is_file()]

    hashes: set[str] = set()
    dups: dict[str, list[Path]] = {}

    for f in files:
        h = get_sha256(f)
        if h in hashes:
            dups[h].append(f)
        else:
            dups[h] = [f]
            hashes.add(h)

    for h, fs in dups.items():
        if len(fs) < 2:
            continue

        sort_by_date = sorted(fs, key=lambda f: f.stat().st_mtime)

        to_delete = sort_by_date[1:]
        if delete == "old":
            to_delete = sort_by_date[:-1]

        print("\nDuplicates:")
        for f in fs:
            print(f, "(", datetime.fromtimestamp(f.stat().st_mtime), ")")
        print("")

        print(f'To delete ({"newest" if delete == "new" else "oldest"}):')
        for f in to_delete:
            print(f)
        print("")

        for f in to_delete:
            print(f"rm {f}")
            if not dry_run:
                if yes or click.confirm(f"Delete {f}?", default=True):
                    f.unlink()


if __name__ == "__main__":
    dup()
