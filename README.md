# Discord Cache Viewer

Browse all images cached by Discord in a local, Discord-styled gallery UI.

## Requirements

- Python 3.9+
- Discord installed on Windows

## Usage

```bat
python server.py
```

The app opens automatically at `http://localhost:8765`.

1. Click **Extract Cache** — scans `%AppData%\discord\Cache\Cache_Data` and pulls out every image.
2. Browse the gallery, filter by type (PNG / JPG / GIF / WebP), or search by filename.
3. Click any image to open the lightbox — use arrow keys or the nav buttons to browse.
4. Click **Download** in the lightbox to save an image.

Extracted images are saved to `extracted/` (git-ignored) and deduplicated by content hash.

## Supported Discord variants

- Discord stable (`%AppData%\discord`)
- Discord PTB (`%AppData%\discordptb`)
- Discord Canary (`%AppData%\discordcanary`)

## Notes

- Only reads cache — never modifies Discord files.
- Images are extracted from raw Chromium cache blocks using magic-byte detection; some incomplete cache entries may appear broken.
- Re-running extraction is idempotent (duplicate files are skipped).
