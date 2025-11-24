import os

import cairosvg


def convert_svg_to_png():
    """SVGファイルをPNG形式に変換します。"""
    input_file_path = r"C:\Shinseikai\IconFlow\input\app.svg"
    output_file_path = r"C:\Shinseikai\IconFlow\processing\app.png"

    # 出力先ディレクトリが存在しない場合は作成
    output_dir = os.path.dirname(output_file_path)
    os.makedirs(output_dir, exist_ok=True)

    try:
        cairosvg.svg2png(
            url=input_file_path,
            write_to=output_file_path
        )
        print(f"変換が完了しました: {output_file_path}")
    except FileNotFoundError as e:
        print(f"エラー: 入力ファイルが見つかりません: {input_file_path}")
        raise
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        raise


if __name__ == "__main__":
    convert_svg_to_png()