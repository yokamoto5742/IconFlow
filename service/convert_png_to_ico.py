from PIL import Image

from utils.config_manager import load_config


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


def main():
    """メイン処理"""
    config = load_config()
    png_input = config.get('Paths', 'png_file_path')
    ico_output = config.get('Paths', 'ico_file_path')
    icon_size = config.getint('Icon', 'icon_size')

    try:
        convert_png_to_ico(png_input, ico_output, size=icon_size)
    except FileNotFoundError:
        print(f"\nエラー: {png_input} が見つかりません。")
        print("\nSVGファイルをPNGに変換してください:")


if __name__ == "__main__":
    main()
