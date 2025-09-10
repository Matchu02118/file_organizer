# File Organizer

A small desktop application to organize files in a folder using two modes:
- General File Organizer — organizes files by category (Images, Documents, Code, etc.).
- Name-Based Documents Organizer — moves files that match a provided first/last name into a personal folder structure. It only supports Documents, Records, and Images. (See "Supported Categories" section).

Built with Python and PyQt6.

## Features

- Option 1 — General File Organizer
  - Organizes files into category folders (Executables, Documents, Records, Images, Audio, Videos, Archives, Code).
  - Unsupported or unknown extensions are placed in `Others`.
  - Select the working directory with the folder icon next to the input field.
  - Toggle categories on/off to exclude/include those extensions from the organization process. A popup shows which extensions will be ignored or included.

- Option 2 — Name-Based Documents Organizer
  - Focused on personal files (documents, images, records).
  - Moves files that match the provided first and last name into a folder named `Last, First`.
  - Filename matching is strict and case-insensitive (e.g. `John Doe.pdf`, `Doe, John B.png`, `JohnDoe.txt` → `Doe, John` folder).
  - Select the working directory the same way as in Option 1.

## Supported categories
- Executables: `.exe`, `.msi`, `.sh`, `.bat`, `.apk`
- Documents: `.docx`, `.doc`, `.pdf`, `.txt`, `.odt`
- Records: `.xlsx`, `.xls`, `.csv`
- Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`
- Audio: `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`, `.m4a`
- Videos: `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`
- Archives: `.zip`, `.rar`, `.tar`, `.gz`, `.7z`
- Code: `.py`, `.java`, `.cpp`, `.c`, `.js`, `.ts`, `.html`, `.css`, `.rb`, `.php`, `.go`, `.rs`
- Other extensions are grouped under `Others`.

## Requirements

- Python 3.8+
- PyQt6

Optional:
- PyInstaller (to build a standalone executable)

## Installation (Windows)

1. Create and activate a virtual environment (recommended):
   - python -m venv venv
   - venv\Scripts\activate

2. Install PyQt6:
   - pip install PyQt6

3. (If you use resource compilation) ensure resource files (icons, .qrc) are available or the `resources` module is present.

## Run

From the project folder:
- python main.py

The main window opens with two options. Use the folder icon to pick the working directory and follow on-screen prompts.

## Usage Notes

- Always back up important files before running the organizer on a large folder.
- Option 1 moves all files (subject to excluded categories) into a new folder named `MyOrganizedFiles-<MM-DD-YYYY>` by default (can be changed inside the app).
- Option 2 creates a folder `Last, First` and organizes matched files into category subfolders.
- If a file with the same name exists in the destination, a numeric suffix (_1, _2, ...) is appended.

## Credits

- FontAwesome — Icons  
- FreePik — Icons & Images  
- Vecteezy — Icons & Images  
- Patrick Loeber (python-engineer.com) — Inspiration for the file-organizing logic  
- Canva — Button design assets
