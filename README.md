<p align="center">
  <img src="assets/banner.svg" alt="Discord Cache Viewer" width="900"/>
</p>

<p align="center">
  A local gallery viewer for images cached by Discord on Windows.<br/>
  Dark-themed, keyboard-friendly, and fully offline — no Discord API, no login.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-5865f2?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Platform-Windows-0078d4?style=flat-square&logo=windows&logoColor=white"/>
  <img src="https://img.shields.io/badge/Dependencies-Zero-23a55a?style=flat-square"/>
  <img src="https://img.shields.io/badge/Repo-Public-23a55a?style=flat-square"/>
  <img src="https://img.shields.io/badge/⚠%EF%B8%8F%20Unofficial-Not%20affiliated%20with%20Discord-faa61a?style=flat-square"/>
</p>

> **Unofficial project.** Not affiliated with, endorsed by, or associated with Discord Inc. in any way. Discord and the Discord logo are trademarks of Discord Inc.

---

## Quick start

```bat
git clone https://github.com/jabreeflor/discord-cache-viewer
cd discord-cache-viewer
python server.py
```

Browser opens automatically at **http://localhost:8765**. Hit **Extract Cache** and your images load in seconds.

---

## Features

- **One-click extraction** — scans `%AppData%\discord\Cache\Cache_Data` and pulls out every JPEG, PNG, GIF, and WebP
- **Content-hash deduplication** — re-running extraction is safe; no duplicate files ever written
- **Filterable gallery** — filter by type (PNG / JPG / GIF / WebP) or search by filename
- **Lightbox** — click any image to open full-size; navigate with `←` `→`, close with `Esc`
- **Download button** — save any image directly from the lightbox
- **Discord variants** — auto-detects stable, PTB, and Canary installs

---

## How it works

Discord (like all Chromium-based apps) caches remote resources in a binary block format with no file extensions. This tool scans those blocks for known image magic bytes — `FF D8 FF` (JPEG), `89 PNG` (PNG), `RIFF…WEBP` (WebP), `GIF8` (GIF) — extracts the image data starting at that offset, and saves it to `extracted/` using an MD5 content hash as the filename.

The local HTTP server (`server.py`) serves the gallery UI and proxies the extracted images — nothing ever leaves your machine.

---

## Notes

- Read-only — Discord's cache files are never modified.
- Some cache entries may be incomplete (partial downloads); those images will appear broken in the gallery.
- `extracted/` is git-ignored and safe to delete at any time.
