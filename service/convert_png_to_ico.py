from PIL import Image


def convert_png_to_ico(png_path: str, ico_path: str, size: int = 128) -> None:
    """
    PNG画像をICOファイルに変換します

    Args:
        png_path: 入力PNGファイルのパス
        ico_path: 出力ICOファイルのパス
        size: アイコンのサイズ（ピクセル）
    """
    print(f"PNG→ICO変換: サイズ指定 {size}x{size}")
    original_image = Image.open(png_path)
    print(f"元のPNG画像サイズ: {original_image.size}")
    resized_image = original_image.resize((size, size), Image.Resampling.LANCZOS)

    resized_image.save(ico_path, format='ICO', sizes=[(size, size)])

    print(f"変換完了: {png_path} -> {ico_path}")
    print(f"出力ICOサイズ: {size}x{size} のみ")
