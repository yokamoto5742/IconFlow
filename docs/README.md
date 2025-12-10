# IconFlow

SVGファイルをPNGまたはICO形式に変換するUIアプリケーション

**バージョン**: 1.0.2
**更新日**: 2025年12月10日

## 主な特徴

- SVG → PNG変換（CairoSVG使用）
- PNG → ICO変換（Pillow使用、サイズ指定対応）
- SVG → ICO直接変換
- シンプルなGUIで簡単操作
- 設定ファイルによるカスタマイズ
- PyInstaller対応実行ファイル化

## 必要な環境

- Python 3.12以上
- Windows 11
- GTK3ランタイム（CairoSVG用）

## インストール

### 1. GTK3ランタイムをインストール

CairoSVGが必要とするGTK3ランタイムをダウンロード・インストール：

[GTK-for-Windows-Runtime-Environment-Installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)

### 2. リポジトリをクローン

```bash
git clone https://github.com/your-username/IconFlow.git
cd IconFlow
```

### 3. 仮想環境を作成・有効化

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 4. 依存ライブラリをインストール

```bash
pip install -r requirements.txt
```

### 5. 設定ファイルを編集

`utils/config.ini`を環境に合わせて編集：

```ini
[Appearance]
font_size = 11
window_width = 250
window_height = 300

[Paths]
downloads_path = C:\Users\YourUsername\Downloads
output_path = C:\Your\Output\Path

[Icon]
icon_size = 128        # SVG→PNG変換用サイズ
ico_size = 128         # PNG→ICO変換用サイズ
```

## 使用方法

### アプリケーション起動

```bash
python main.py
```

GUIで以下の変換が可能：

- **SVGからPNGへ** - SVG → PNG変換
- **PNGからicoへ** - PNG → ICO変換
- **SVGからicoへ** - SVG → ICO直接変換（2段階）
- **設定ファイル** - config.iniをメモ帳アプリで開く
- **閉じる** - アプリを終了

### 変換の流れ

1. ボタンをクリック
2. ファイル選択ダイアログでファイルを選択（初期フォルダはconfig.ini内のdownloads_path）
3. 自動的に変換実行（コンソールにログが出力）
4. 変換完了後、出力フォルダを自動で開く

## プロジェクト構造

```
IconFlow/
├── app/
│   ├── __init__.py              # バージョン情報
│   └── main_window.py           # GUIメインウィンドウ
├── service/
│   ├── convert_svg_to_png.py   # SVG→PNG変換関数
│   └── convert_png_to_ico.py   # PNG→ICO変換関数
├── utils/
│   ├── config_manager.py        # 設定ファイル管理
│   └── config.ini               # アプリケーション設定
├── scripts/
│   ├── version_manager.py       # バージョン管理
│   └── project_structure.py     # 構造ドキュメント生成
├── tests/                       # テストファイル
├── assets/                      # アイコン・画像ファイル
├── main.py                      # エントリーポイント
├── build.py                     # PyInstallerビルドスクリプト
└── requirements.txt             # 依存ライブラリリスト
```

## 主要機能

### SVG → PNG変換

CairoSVGを使用した高品質なSVG→PNG変換。サイズ指定に対応。

```python
from service.convert_svg_to_png import convert_svg_to_png

convert_svg_to_png(
    input_file_path="input.svg",
    output_file_path="output.png",
    output_size=128
)
```

**パラメータ**:
- `input_file_path`: 入力SVGファイルパス
- `output_file_path`: 出力PNGファイルパス
- `output_size`: 出力サイズ（ピクセル、省略可）

### PNG → ICO変換

Pillowを使用したPNG→ICO変換。指定サイズでリサイズして保存。

```python
from service.convert_png_to_ico import convert_png_to_ico

convert_png_to_ico(png_path="input.png", ico_path="output.ico")
```

**パラメータ**:
- `png_path`: 入力PNGファイルパス
- `ico_path`: 出力ICOファイルパス
- `size`: ICOサイズ（ピクセル、デフォルト: 128）

### 設定管理

開発環境とPyInstaller実行ファイルの両方に対応。

```python
from utils.config_manager import load_config

config = load_config()
font_size = config.getint('Appearance', 'font_size')
output_path = config.get('Paths', 'output_path')
icon_size = config.getint('Icon', 'icon_size')
```

## 開発情報

### テスト実行

```bash
python -m pytest tests/ -v --tb=short
```

以下の機能をカバー：
- 設定ファイルの読み書き
- SVG → PNG変換
- PNG → ICO変換
- エラーハンドリング

### 実行ファイルのビルド

```bash
python build.py
```

自動実行内容：
1. `app/__init__.py`のパッチバージョンをインクリメント
2. `docs/README.md`のバージョン情報を更新
3. PyInstallerでビルド（`dist/IconFlow`に出力）

### バージョン情報

`app/__init__.py`に保存：
```python
__version__ = "1.0.2"
__date__ = "2025-12-10"
```

`scripts/version_manager.py`でビルド時に自動更新。

## トラブルシューティング

### 「設定ファイルが見つかりません」エラー

`utils/config.ini`が存在しているか確認し、ファイルパスが正しいか確認してください。

### SVG変換エラー

GTK3ランタイムがインストールされているか確認してください。必要に応じて再インストール：

[GTK-for-Windows-Runtime-Environment-Installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)

### ファイル選択後に変換されない

コンソールでエラーメッセージを確認してください。以下の点を確認：
- SVGファイルが正しい形式
- PNG/ICOファイルのパスがconfig.ini内のoutput_pathと一致

### PyInstallerビルド失敗

すべての依存ライブラリをインストール：

```bash
pip install -r requirements.txt
```

## 変更履歴

詳細な変更履歴は [CHANGELOG.md](./CHANGELOG.md) を参照してください。

## ライセンス

[LICENSE](./LICENSE) を参照してください。
