"""
Discord image cache extractor.
Scans Chromium cache files and extracts images by magic-byte detection.
"""

import os
import hashlib
from pathlib import Path

CACHE_PATHS = [
    Path(os.environ.get("APPDATA", "")) / "discord" / "Cache" / "Cache_Data",
    Path(os.environ.get("LOCALAPPDATA", "")) / "Discord" / "Cache" / "Cache_Data",
    Path(os.environ.get("APPDATA", "")) / "discordptb" / "Cache" / "Cache_Data",
    Path(os.environ.get("APPDATA", "")) / "discordcanary" / "Cache" / "Cache_Data",
]

SIGNATURES = [
    (b"\xff\xd8\xff", ".jpg"),
    (b"\x89PNG\r\n\x1a\n", ".png"),
    (b"GIF87a", ".gif"),
    (b"GIF89a", ".gif"),
    (b"RIFF", ".webp"),
]


def find_discord_cache() -> Path | None:
    for path in CACHE_PATHS:
        if path.exists():
            return path
    return None


def _detect_image(data: bytes) -> tuple[int, str] | None:
    for sig, ext in SIGNATURES:
        idx = data.find(sig)
        if idx == -1:
            continue
        if ext == ".webp":
            if len(data) > idx + 12 and data[idx + 8 : idx + 12] == b"WEBP":
                return idx, ext
        else:
            return idx, ext
    return None


def extract_images(cache_dir: Path, output_dir: Path, progress_cb=None) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    extracted = []

    files = [f for f in cache_dir.iterdir() if f.is_file()]
    total = len(files)

    for i, cache_file in enumerate(files):
        if progress_cb:
            progress_cb(i + 1, total, cache_file.name)
        try:
            data = cache_file.read_bytes()
        except (OSError, PermissionError):
            continue

        result = _detect_image(data)
        if result is None:
            continue

        offset, ext = result
        image_data = data[offset:]

        # Stable filename based on content hash
        digest = hashlib.md5(image_data).hexdigest()
        out_path = output_dir / f"{digest}{ext}"

        if not out_path.exists():
            out_path.write_bytes(image_data)

        extracted.append(out_path)

    return extracted
