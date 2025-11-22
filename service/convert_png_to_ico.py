from PIL import Image

from utils.config_manager import load_config


def convert_png_to_ico(png_path: str, ico_path: str, sizes: list[tuple[int, int]] = None) -> None:
    """
    PNG画像をICOファイルに変換します。

    Args:
        png_path: 入力PNGファイルのパス
        ico_path: 出力ICOファイルのパス
        sizes: ICOに含めるサイズのリスト [(幅, 高さ)]
               Noneの場合、デフォルトのサイズセットを使用
    """
    if sizes is None:
        # Windowsで一般的に使用されるアイコンサイズ
        sizes = [(128, 128)]

    original_image = Image.open(png_path)

    # 各サイズの画像を生成
    images = []
    for width, height in sizes:
        resized_image = original_image.resize((width, height), Image.Resampling.LANCZOS)
        images.append(resized_image)

    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )

    print(f"変換完了: {png_path} -> {ico_path}")
    print(f"含まれるサイズ: {sizes}")


def main():
    """メイン処理"""
    config = load_config()
    png_input = config.get('Paths', 'png_file_path')
    ico_output = config.get('Paths', 'ico_file_path')
    icon_size = config.getint('Icon', 'icon_size')

    try:
        convert_png_to_ico(png_input, ico_output, sizes=[(icon_size, icon_size)])
    except FileNotFoundError:
        print(f"\nエラー: {png_input} が見つかりません。")
        print("\nSVGファイルをPNGに変換してください:")


if __name__ == "__main__":
    main()
