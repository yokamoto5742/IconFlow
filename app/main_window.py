import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

from app import __version__
from service.convert_png_to_ico import convert_png_to_ico
from service.convert_svg_to_png import convert_svg_to_png
from utils.config_manager import CONFIG_PATH, load_config


class IconFlowMainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title(f"IconFlow v{__version__}")

        config = load_config()
        window_width = config.getint('Appearance', 'window_width')
        window_height = config.getint('Appearance', 'window_height')
        font_size = config.getint('Appearance', 'font_size')

        self.root.geometry(f"{window_width}x{window_height}")
        self.root.resizable(False, False)

        button_font = ("Yu Gothic UI", font_size)
        button_width = 20
        button_padx = 10
        button_pady = 10

        btn_svg_to_png = tk.Button(
            self.root,
            text="SVGからPNGへ",
            font=button_font,
            width=button_width,
            command=self.convert_svg_to_png_handler
        )
        btn_svg_to_png.pack(pady=button_pady, padx=button_padx)

        btn_png_to_ico = tk.Button(
            self.root,
            text="PNGからicoへ",
            font=button_font,
            width=button_width,
            command=self.convert_png_to_ico_handler
        )
        btn_png_to_ico.pack(pady=button_pady, padx=button_padx)

        btn_svg_to_ico = tk.Button(
            self.root,
            text="SVGからicoへ",
            font=button_font,
            width=button_width,
            command=self.convert_svg_to_ico_handler
        )
        btn_svg_to_ico.pack(pady=button_pady, padx=button_padx)

        btn_open_config = tk.Button(
            self.root,
            text="設定ファイル",
            font=button_font,
            width=button_width,
            command=self.open_config_handler
        )
        btn_open_config.pack(pady=button_pady, padx=button_padx)

        btn_close = tk.Button(
            self.root,
            text="閉じる",
            font=button_font,
            width=button_width,
            command=self.root.quit
        )
        btn_close.pack(pady=button_pady, padx=button_padx)

    def convert_svg_to_png_handler(self):
        """SVG→PNG変換ボタンのハンドラ"""
        try:
            config = load_config()
            downloads_path = config.get('Paths', 'downloads_path')
            output_path = config.get('Paths', 'output_path')

            # SVGファイルを選択
            svg_file = filedialog.askopenfilename(
                title="SVGファイルを選択",
                initialdir=downloads_path,
                filetypes=[("SVG files", "*.svg"), ("All files", "*.*")]
            )

            if not svg_file:
                return

            # ファイル名（拡張子なし）を取得
            base_name = os.path.splitext(os.path.basename(svg_file))[0]
            png_output = os.path.join(output_path, f"{base_name}.png")

            # 変換実行
            convert_svg_to_png(svg_file, png_output)

            # 出力ディレクトリを開く
            if os.path.exists(output_path):
                os.startfile(output_path)
        except FileNotFoundError as e:
            messagebox.showerror("エラー", f"ファイルが見つかりません:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("エラー", f"変換中にエラーが発生しました:\n{str(e)}")

    def convert_png_to_ico_handler(self):
        """PNG→ico変換ボタンのハンドラ"""
        try:
            config = load_config()
            downloads_path = config.get('Paths', 'downloads_path')
            output_path = config.get('Paths', 'output_path')
            icon_size = config.getint('Icon', 'icon_size')

            # PNGファイルを選択
            png_file = filedialog.askopenfilename(
                title="PNGファイルを選択",
                initialdir=downloads_path,
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )

            if not png_file:
                return

            # ファイル名（拡張子なし）を取得
            base_name = os.path.splitext(os.path.basename(png_file))[0]
            ico_output = os.path.join(output_path, f"{base_name}.ico")

            # 変換実行
            convert_png_to_ico(png_file, ico_output, sizes=[(icon_size, icon_size)])

            # 出力ディレクトリを開く
            if os.path.exists(output_path):
                os.startfile(output_path)
        except FileNotFoundError as e:
            messagebox.showerror("エラー", f"ファイルが見つかりません:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("エラー", f"変換中にエラーが発生しました:\n{str(e)}")

    def convert_svg_to_ico_handler(self):
        """SVG→ico変換ボタンのハンドラ"""
        try:
            config = load_config()
            downloads_path = config.get('Paths', 'downloads_path')
            output_path = config.get('Paths', 'output_path')
            icon_size = config.getint('Icon', 'icon_size')

            # SVGファイルを選択
            svg_file = filedialog.askopenfilename(
                title="SVGファイルを選択",
                initialdir=downloads_path,
                filetypes=[("SVG files", "*.svg"), ("All files", "*.*")]
            )

            if not svg_file:
                return

            # ファイル名（拡張子なし）を取得
            base_name = os.path.splitext(os.path.basename(svg_file))[0]
            png_output = os.path.join(output_path, f"{base_name}.png")
            ico_output = os.path.join(output_path, f"{base_name}.ico")

            # まずSVG→PNG変換
            convert_svg_to_png(svg_file, png_output)

            # 次にPNG→ICO変換
            convert_png_to_ico(png_output, ico_output, sizes=[(icon_size, icon_size)])

            # 出力ディレクトリを開く
            if os.path.exists(output_path):
                os.startfile(output_path)
        except FileNotFoundError as e:
            messagebox.showerror("エラー", f"ファイルが見つかりません:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("エラー", f"変換中にエラーが発生しました:\n{str(e)}")

    def open_config_handler(self):
        """設定ファイルをメモ帳で開く"""
        try:
            if os.path.exists(CONFIG_PATH):
                subprocess.Popen(['notepad.exe', CONFIG_PATH])
            else:
                messagebox.showerror("エラー", f"設定ファイルが見つかりません:\n{CONFIG_PATH}")
        except Exception as e:
            messagebox.showerror("エラー", f"設定ファイルを開けませんでした:\n{str(e)}")


def run():
    """アプリケーションを起動"""
    root = tk.Tk()
    IconFlowMainWindow(root)
    root.mainloop()
