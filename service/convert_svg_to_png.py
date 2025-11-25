from typing import Optional

import cairosvg  # type: ignore[import-not-found]


def convert_svg_to_png(input_file_path: Optional[str] = None, output_file_path: Optional[str] = None) -> Optional[str]:
    """SVGファイルをPNG形式に変換します

    Args:
        input_file_path: 入力SVGファイルのパス
        output_file_path: 出力PNGファイルのパス
    """

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
