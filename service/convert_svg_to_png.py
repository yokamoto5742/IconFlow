import os

import cairosvg

from utils.config_manager import load_config


def convert_svg_to_png(input_file_path: str = None, output_file_path: str = None):
    """SVGファイルをPNG形式に変換します

    Args:
        input_file_path: 入力SVGファイルのパス。Noneの場合はconfigから取得
        output_file_path: 出力PNGファイルのパス。Noneの場合はconfigから取得
    """
    config = load_config()

    if input_file_path is None:
        input_file_path = config.get('Paths', 'input_file_path')
    if output_file_path is None:
        output_file_path = config.get('Paths', 'png_file_path')

    # 出力先ディレクトリが存在しない場合は作成
    output_dir = os.path.dirname(output_file_path)
    os.makedirs(output_dir, exist_ok=True)

    try:
        cairosvg.svg2png(
            url=input_file_path,
            write_to=output_file_path
        )
        print(f"変換が完了しました: {output_file_path}")
        return output_file_path
    except FileNotFoundError as e:
        print(f"エラー: 入力ファイルが見つかりません: {input_file_path}")
        raise
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        raise


if __name__ == "__main__":
    convert_svg_to_png()