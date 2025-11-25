# IconFlow

SVGファイルをPNGおよびICO形式に変換するPython GUIアプリケーションです。

**現在のバージョン**: 1.0.1
**最終更新日**: 2025年11月25日

## 主な特徴

- SVG to PNG変換（CairoSVGを使用）
- PNG to ICO変換（Pillowを使用）
- SVG to ICO直接変換
- GUI操作で簡単にファイル変換可能
- 設定ファイルによるカスタマイズ
- PyInstallerによる実行ファイル化対応

## 必要な環境

- Python 3.12以上
- Windows11

## 必須依存ライブラリ

- `CairoSVG` - SVGからPNGへの変換
- `Pillow` - PNG操作とICO変換
- `tkinter` - GUI（Python標準ライブラリに含まれます）

その他の依存ライブラリは`requirements.txt`を参照してください。

## インストール

### 1. リポジトリのクローン

```bash
git clone https://github.com/your-username/IconFlow.git
cd IconFlow
```

### 2. 仮想環境の作成と有効化

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 4. 設定ファイルのセットアップ

`utils/config.ini`を編集して、ファイルパスを環境に合わせて設定します：

```ini
[Appearance]
font_size = 11
window_width = 250
window_height = 300

[Paths]
downloads_path = C:\Users\YourUsername\Downloads
output_path = C:\Your\Output\Path

[Icon]
icon_size = 128
```

## 使用方法

### アプリケーション起動

```bash
python main.py
```

GUIウィンドウが起動し、以下の操作が可能になります：

- **SVGからPNGへ** - SVGファイルをPNG形式に変換
- **PNGからicoへ** - PNG画像をICO形式に変換
- **SVGからicoへ** - SVGファイルを直接ICO形式に変換
- **設定ファイル** - config.iniをメモ帳で編集
- **閉じる** - アプリケーションを終了

### 変換処理の流れ

1. ボタンをクリックして対象ファイルを選択
2. 「downloads_path」から初期フォルダが開きます
3. ファイルを選択すると自動的に変換が実行されます
4. 変換完了後、出力フォルダが自動で開きます

## プロジェクト構造

```
IconFlow/
├── app/
│   ├── __init__.py              # バージョン情報
│   └── main_window.py           # GUIメインウィンドウクラス
├── service/
│   ├── convert_svg_to_png.py   # SVG→PNG変換関数
│   └── convert_png_to_ico.py   # PNG→ICO変換関数
├── utils/
│   ├── config_manager.py        # 設定ファイル管理
│   └── config.ini               # アプリケーション設定
├── scripts/
│   ├── version_manager.py       # バージョン管理ユーティリティ
│   └── project_structure.py     # プロジェクト構造生成
├── tests/                       # テストファイル
├── assets/
│   ├── IconFlow.ico             # アプリケーションアイコン
│   └── IconFlow.svg             # SVGソース
├── main.py                      # エントリーポイント
├── build.py                     # PyInstallerビルドスクリプト
└── requirements.txt             # Python依存ライブラリ
```

## 主要機能の詳細

### SVG to PNG変換

`service/convert_svg_to_png.py`で実装されています。CairoSVGを使用して高品質なPNG変換を行います。

```python
from service.convert_svg_to_png import convert_svg_to_png

convert_svg_to_png(
    input_file_path="path/to/file.svg",
    output_file_path="path/to/output.png"
)
```

### PNG to ICO変換

`service/convert_png_to_ico.py`で実装されています。Pillowを使用してPNG画像をICO形式に変換し、指定サイズにリサイズします。

```python
from service.convert_png_to_ico import convert_png_to_ico

convert_png_to_ico(png_path="path/to/file.png", ico_path="path/to/output.ico")
```

**パラメータ**:
- `png_path`: 入力PNGファイルのパス
- `ico_path`: 出力ICOファイルのパス
- `size`: アイコンサイズ（デフォルト: 128ピクセル）

### 設定管理

`utils/config_manager.py`は開発環境とPyInstallerでビルドされた実行ファイルの両方に対応しています。

```python
from utils.config_manager import load_config, save_config

config = load_config()
font_size = config.getint('Appearance', 'font_size')
downloads_path = config.get('Paths', 'downloads_path')
```

### メインウィンドウ

`app/main_window.py`の`IconFlowMainWindow`クラスがGUI処理を担当します。
設定から読み込んだ値に基づいてウィンドウを構成し、各変換ボタンのイベント処理を管理します。

## 開発情報

### テスト実行

```bash
python -m pytest tests/ -v --tb=short
```

テストでは以下の機能をカバーしています：
- 設定ファイルの読み書き
- SVG to PNG変換
- PNG to ICO変換
- GUIウィンドウの初期化
- エラーハンドリング

### 実行ファイルのビルド

```bash
python build.py
```

このコマンドは以下の処理を自動的に実行します：

1. `app/__init__.py`のパッチバージョンをインクリメント
2. `docs/README.md`のバージョン情報を更新
3. PyInstallerを使用して実行ファイルをビルド
4. `dist/IconFlow`に実行ファイルを生成

### バージョン管理

バージョン情報は`app/__init__.py`に保存されます：

```python
__version__ = "1.0.1"
__date__ = "2025-11-25"
```

`scripts/version_manager.py`を通じて、ビルド時に自動的にパッチバージョンがインクリメントされ、READMEのバージョン情報も同期されます。

### プロジェクト構造ドキュメント生成

```bash
python scripts/project_structure.py -o project_structure.txt
```

プロジェクトの構造を自動生成してテキストファイルに出力します。

## トラブルシューティング

### 「設定ファイルが見つかりません」エラー

**原因**: `utils/config.ini`が見つからない場合に発生します。

**解決方法**:
- `utils`ディレクトリにconfig.iniが存在することを確認
- ファイルパスが正しく設定されているか確認

### SVG変換時の「ファイルが見つかりません」エラー

**原因**: 指定されたSVGファイルが存在しないか、パスが間違っている可能性があります。

**解決方法**:
- ファイルが実際に存在することを確認
- ファイルパスに日本語が含まれている場合は、エンコーディングに注意

### 変換後の画像が不正な形式

**原因**: CairoSVGやPillowのバージョン不整合、またはSVGファイルの形式が不正の可能性があります。

**解決方法**:
- `pip install --upgrade CairoSVG Pillow`で最新版に更新
- SVGファイルが正しい形式であることを確認
- 簡単なSVGファイルで試して動作を確認

### PyInstallerビルド失敗

**原因**: 依存ライブラリが不足しているか、パスの問題の可能性があります。

**解決方法**:
- すべての依存ライブラリがインストールされているか確認
- `pip install -r requirements.txt`を再実行
- 仮想環境を作り直して再度ビルドを試行

## 変更履歴

詳細な変更履歴は [CHANGELOG.md](./CHANGELOG.md) を参照してください。

## ライセンス

[LICENSE](./LICENSE) を参照してください。
