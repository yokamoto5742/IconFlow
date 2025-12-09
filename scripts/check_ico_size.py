"""ICOファイルのサイズ情報を確認するスクリプト"""
from PIL import Image

ico_path = r"C:\Shinseikai\IconFlow\output\IconFlow.ico"

try:
    ico = Image.open(ico_path)
    print(f"ファイル: {ico_path}")
    print(f"デフォルトサイズ: {ico.size}")
    print(f"含まれるサイズ一覧: {ico.info.get('sizes', 'N/A')}")
except FileNotFoundError:
    print(f"ファイルが見つかりません: {ico_path}")
except Exception as e:
    print(f"エラー: {e}")
