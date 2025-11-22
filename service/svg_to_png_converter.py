import cairosvg


def convert_svg_to_png():
    """SVGファイルをPNG形式に変換します。"""
    input_file_path = r"C:\Shinseikai\IconFlow\input\app.svg"
    output_file_path = r"C:\Shinseikai\IconFlow\processing\app.png"

    try:
        cairosvg.svg2png(
            url=input_file_path,
            write_to=output_file_path
        )
        print(f"変換が完了しました: {output_file_path}")
    except FileNotFoundError:
        print(f"エラー: 入力ファイルが見つかりません: {input_file_path}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    convert_svg_to_png()