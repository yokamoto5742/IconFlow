# Changelog

このプロジェクトの全ての著しい変更は、このファイルに記録されます。

このファイルのフォーマットは[Keep a Changelog](https://keepachangelog.com/ja/1.1.0/)に基づいており、このプロジェクトは[Semantic Versioning](https://semver.org/lang/ja/)を遵守しています。

## [Unreleased]

## [1.0.2] - 2025-12-10

### Added
- 変換処理のログ出力機能
  - SVG→PNG変換時のサイズ指定ログ
  - PNG→ICO変換時のサイズ指定ログ
  - 元のPNG画像サイズの表示
  - 出力ICOサイズの表示

### Changed
- ICO変換処理を改善し、`sizes`パラメータを指定してICO形式の仕様に準拠
- config.ini の ICO設定にコメントを追加（SVG→PNG変換用 と PNG→ICO変換用の区分け）
- SVG→PNG変換でサイズ指定がない場合のログ出力を追加

## [1.0.1] - 2025-11-25

### Added
- GTK3ランタイムのインストール方法をドキュメント化
- テストスイート（config_manager、main、main_window、convert_png_to_ico、convert_svg_to_pngのテスト）

### Changed
- 型ヒントを utils/config_manager と service/convert_svg_to_png に追加
- utils/config_manager で _MEIPASS の存在チェックを安全に処理
- service/convert_svg_to_png の引数を Optional に変更

## [1.0.0] - 2025-11-24

### Added
- SVGからPNGへの変換機能（CairoSVG使用）
- PNGからICOへの変換機能（Pillow使用）
- GUIアプリケーション（tkinter使用）
- ファイル選択ダイアログ
- 変換後に実行ディレクトリを開く機能
- 設定ファイル（config.ini）管理機能
  - ウィンドウサイズ設定
  - アイコンサイズ設定
  - ファイルパス設定
- PyInstaller対応のビルドスクリプト
- エラーハンドリングと日本語エラーメッセージ
- プロジェクト構造ドキュメント生成スクリプト
- バージョン管理スクリプト
- プロジェクトドキュメント（README.md）
- アプリケーションアイコン

### Changed
- メインウィンドウクラスを MainWindow から IconFlowMainWindow に変更
- GUI処理を main.py に集約
- PNG to ICO変換処理を単純化
- 共通処理をヘルパーメソッド化
- 不要な設定読み込みを削除

### Fixed
- エラーハンドリングの改善
- 出力パスの区切り文字を修正
- バージョン 1.0.0 への初期設定

[Unreleased]: https://github.com/yokamkondo/IconFlow/compare/v1.0.1...HEAD
[1.0.2]: https://github.com/yokamkondo/IconFlow/compare/v1.0.0...v1.0.1
[1.0.1]: https://github.com/yokamkondo/IconFlow/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/yokamkondo/IconFlow/releases/tag/v1.0.0
