import os
import subprocess
import tkinter as tk
from tkinter import messagebox

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
            convert_svg_to_png()
            messagebox.showinfo("成功", "SVGからPNGへの変換が完了しました")
        except FileNotFoundError as e:
            messagebox.showerror("エラー", f"ファイルが見つかりません:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("エラー", f"変換中にエラーが発生しました:\n{str(e)}")

    def convert_svg_to_ico_handler(self):
        """SVG→ico変換ボタンのハンドラ"""
        try:
            # まずSVG→PNG変換
            convert_svg_to_png()

            # 次にPNG→ICO変換
            config = load_config()
            png_input = config.get('Paths', 'png_file_path')
            ico_output = config.get('Paths', 'ico_file_path')
            icon_size = config.getint('Icon', 'icon_size')

            convert_png_to_ico(png_input, ico_output, sizes=[(icon_size, icon_size)])
            messagebox.showinfo("成功", "SVGからICOへの変換が完了しました")
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
