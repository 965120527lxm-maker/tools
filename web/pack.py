"""Copy or archive a static web site folder (deck bundle)."""

from __future__ import annotations

import argparse
import shutil
import tarfile
from pathlib import Path

# Default names included when packing a deck site (rest copied if present).
DEFAULT_SITE_FILES = ("deck.html", "index.html", "data.json", "outline.html")
DEFAULT_SITE_DIRS = ("figures", "assets")


def site_paths(root: Path) -> list[Path]:
    """List relative paths that belong to a deployable site under root."""
    found: list[Path] = []
    for name in DEFAULT_SITE_FILES:
        p = root / name
        if p.is_file():
            found.append(p)
    for name in DEFAULT_SITE_DIRS:
        d = root / name
        if d.is_dir():
            for f in sorted(d.rglob("*")):
                if f.is_file():
                    found.append(f)
    return found


def copy_site(src: Path, dst: Path, *, clean: bool = False) -> Path:
    """Copy site bundle: html/json + figures/ + assets/."""
    src = src.resolve()
    dst = dst.resolve()
    if not src.is_dir():
        raise FileNotFoundError(f"not a directory: {src}")

    paths = site_paths(src)
    if not paths:
        raise FileNotFoundError(f"no site files under {src} (expected deck.html etc.)")

    if dst.exists():
        if clean:
            shutil.rmtree(dst)
        elif dst.is_file():
            raise FileExistsError(dst)
    dst.mkdir(parents=True, exist_ok=True)

    for p in paths:
        rel = p.relative_to(src)
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, out)

    return dst


def archive_site(src: Path, archive: Path) -> Path:
    """Create .tar.gz of the site bundle."""
    src = src.resolve()
    archive = archive.resolve()
    paths = site_paths(src)
    if not paths:
        raise FileNotFoundError(f"no site files under {src}")

    archive.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "w:gz") as tar:
        for p in paths:
            tar.add(p, arcname=p.relative_to(src).as_posix())
    return archive


def add_pack_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "pack",
        help="copy or archive a site folder (deck.html + figures/ + …)",
    )
    p.add_argument("source", help="site root directory, e.g. docs/progress")
    p.add_argument(
        "dest",
        nargs="?",
        help="destination directory (default: print paths only with --dry-run)",
    )
    p.add_argument(
        "--archive",
        metavar="FILE.tar.gz",
        help="write tar.gz instead of copying to dest",
    )
    p.add_argument(
        "--clean",
        action="store_true",
        help="remove destination directory before copy",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="list files that would be packed",
    )


def run_pack(args: argparse.Namespace) -> int:
    src = Path(args.source)
    paths = site_paths(src)
    if not paths:
        print(f"error: no site files under {src}", flush=True)
        return 1

    rels = [p.relative_to(src) for p in paths]
    if args.dry_run:
        print(f"site bundle under {src} ({len(rels)} files):")
        for r in rels:
            print(f"  {r}")
        return 0

    if args.archive:
        out = archive_site(src, Path(args.archive))
        print(f"archived {len(rels)} files → {out}")
        return 0

    if not args.dest:
        print("error: dest or --archive required (or use --dry-run)", flush=True)
        return 1

    out = copy_site(src, Path(args.dest), clean=args.clean)
    print(f"copied {len(rels)} files → {out}")
    print(f"  serve: python -m tools.web serve {out} --open deck.html")
    return 0
