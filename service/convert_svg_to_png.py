from typing import Optional

import cairosvg


def convert_svg_to_png(input_file_path: Optional[str] = None, output_file_path: Optional[str] = None, output_size: Optional[int] = None) -> Optional[str]:
    """SVGファイルをPNG形式に変換します

    Args:
        input_file_path: 入力SVGファイルのパス
        output_file_path: 出力PNGファイルのパス
        output_size: 出力PNGのサイズ（ピクセル）
    """

    try:
        kwargs = {
            'url': input_file_path,
            'write_to': output_file_path
        }
        if output_size is not None:
            kwargs['output_width'] = output_size
            kwargs['output_height'] = output_size
            print(f"SVG→PNG変換: サイズ指定 {output_size}x{output_size}")
        else:
            print("SVG→PNG変換: サイズ指定なし（元のサイズを使用）")

        cairosvg.svg2png(**kwargs)
        print(f"変換が完了しました: {output_file_path}")
        return output_file_path
    except FileNotFoundError as e:
        print(f"エラー: 入力ファイルが見つかりません: {input_file_path}")
        raise
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        raise
