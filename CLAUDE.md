# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## House Rules:
- 文章ではなくパッチの差分を返す。
- コードの変更範囲は最小限に抑える。
- コードの修正は直接適用する。
- Pythonのコーディング規約はPEP8に従います。
- KISSの原則に従い、できるだけシンプルなコードにします。
- 可読性を優先します。一度読んだだけで理解できるコードが最高のコードです。
- Pythonのコードのimport文は以下の適切な順序に並べ替えてください。
標準ライブラリ
サードパーティライブラリ
カスタムモジュール 
それぞれアルファベット順に並べます。importが先でfromは後です。

## CHANGELOG
このプロジェクトにおけるすべての重要な変更は日本語でdcos/CHANGELOG.mdに記録します。
フォーマットは[Keep a Changelog](https://keepachangelog.com/ja/1.1.0/)に基づきます。

## Automatic Notifications (Hooks)
自動通知は`.claude/settings.local.json` で設定済：
- **Stop Hook**: ユーザーがClaude Codeを停止した時に「作業が完了しました」と通知
- **SessionEnd Hook**: セッション終了時に「Claude Code セッションが終了しました」と通知

## クリーンコードガイドライン
- 関数のサイズ：関数は50行以下に抑えることを目標にしてください。関数の処理が多すぎる場合は、より小さなヘルパー関数に分割してください。
- 単一責任：各関数とモジュールには明確な目的が1つあるようにします。無関係なロジックをまとめないでください。
- 命名：説明的な名前を使用してください。`tmp` 、`data`、`handleStuff`のような一般的な名前は避けてください。例えば、`doCalc`よりも`calculateInvoiceTotal` の方が適しています。
- DRY原則：コードを重複させないでください。類似のロジックが2箇所に存在する場合は、共有関数にリファクタリングしてください。それぞれに独自の実装が必要な場合はその理由を明確にしてください。
- コメント:分かりにくいロジックについては説明を加えます。説明不要のコードには過剰なコメントはつけないでください。
- コメントとdocstringは必要最小限に日本語で記述し、文末に"。"や"."をつけないでください。

## Project Overview

IconFlow is a Python GUI application for converting SVG files to PNG and ICO formats. It uses tkinter for the GUI, CairoSVG for SVG to PNG conversion, and Pillow for PNG to ICO conversion.

## Project Structure

- `app/` - GUI application code (currently minimal/empty main_window.py)
- `service/` - Core conversion services
  - `convert_svg_to_png.py` - SVG to PNG conversion using CairoSVG
  - `convert_png_to_ico.py` - PNG to ICO conversion using Pillow
- `utils/` - Utility modules
  - `config_manager.py` - Configuration file management with PyInstaller support
  - `config.ini` - Application settings (font size, window dimensions, file paths)
- `scripts/` - Build and maintenance scripts
  - `version_manager.py` - Version and date management in app/__init__.py and docs/README.md
  - `project_structure.py` - Project structure documentation generator
- `tests/` - Test files
- `main.py` - Application entry point (currently empty/minimal)
- `build.py` - PyInstaller build script

## Development Commands

### Running the Application
```bash
python main.py
```

### Building Executable
```bash
python build.py
```
This will:
1. Auto-increment the patch version in `app/__init__.py`
2. Update the version and date in `docs/README.md`
3. Build the executable using PyInstaller with windowed mode and icon

### Running Tests
```bash
python -m pytest tests/ -v --tb=short
```

### Generating Project Structure Documentation
```bash
python scripts/project_structure.py -o project_structure.txt
```

## Configuration Management

The application uses `utils/config.ini` for configuration:
- `[Appearance]` - UI settings (font_size, window_width, window_height)
- `[Paths]` - File paths for input SVG, intermediate PNG, and output ICO

The `config_manager.py` handles both development and PyInstaller frozen executable contexts:
- Development: Reads from `utils/config.ini`
- Frozen: Reads from `sys._MEIPASS/config.ini` (bundled by PyInstaller)

## Version Management

Version information is stored in `app/__init__.py`:
```python
__version__ = "x.y.z"
__date__ = "YYYY-MM-DD"
```

The `scripts/version_manager.py` module automatically:
- Increments the patch version
- Updates the date to current timestamp
- Syncs version info to `docs/README.md`

This is automatically called by `build.py` before each build.

## PyInstaller Build Configuration

The build process bundles:
- Main script: `main.py`
- Icon: `assets/app.ico`
- Config file: `utils/config.ini` (bundled to root of executable)
- Windowed mode (no console)
- Output name: `IconFlow`

## Code Style Notes

- Japanese comments are used throughout the codebase for local development
- Error handling includes user-friendly Japanese error messages
- File paths in config use Windows-style absolute paths (e.g., `C:\Shinseikai\IconFlow\...`)
