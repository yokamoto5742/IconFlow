from PIL import Image


def convert_png_to_ico(png_path: str, ico_path: str, size: int = 128) -> None:
    """
    PNG画像をICOファイルに変換します

    Args:
        png_path: 入力PNGファイルのパス
        ico_path: 出力ICOファイルのパス
        size: アイコンのサイズ（ピクセル）
    """
    original_image = Image.open(png_path)
    resized_image = original_image.resize((size, size), Image.Resampling.LANCZOS)
    resized_image.save(ico_path, format='ICO')

    print(f"変換完了: {png_path} -> {ico_path}")
