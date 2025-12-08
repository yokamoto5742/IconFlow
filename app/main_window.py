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

    def _select_file(self, title, filetypes, initialdir):
        """ファイル選択ダイアログを表示"""
        return filedialog.askopenfilename(
            title=title,
            initialdir=initialdir,
            filetypes=filetypes
        )

    def _get_base_name(self, file_path):
        """ファイルのベース名（拡張子なし）を取得"""
        return os.path.splitext(os.path.basename(file_path))[0]

    def _open_output_directory(self, output_path):
        """出力ディレクトリを開く"""
        if os.path.exists(output_path):
            os.startfile(output_path)

    def _handle_errors(self, func):
        """エラーハンドリングを実行"""
        try:
            func()
        except FileNotFoundError as e:
            messagebox.showerror("エラー", f"ファイルが見つかりません:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("エラー", f"変換中にエラーが発生しました:\n{str(e)}")

    def _process_svg_to_png_conversion(self):
        """SVG→PNG変換処理"""
        config = load_config()
        downloads_path = config.get('Paths', 'downloads_path')
        output_path = config.get('Paths', 'output_path')
        icon_size = config.getint('Icon', 'icon_size')

        svg_file = self._select_file(
            "SVGファイルを選択",
            [("SVG files", "*.svg"), ("All files", "*.*")],
            downloads_path
        )

        if not svg_file:
            return

        base_name = self._get_base_name(svg_file)
        png_output = os.path.join(output_path, f"{base_name}.png")

        convert_svg_to_png(svg_file, png_output, icon_size)
        self._open_output_directory(output_path)

    def convert_svg_to_png_handler(self):
        """SVG→PNG変換ボタンのハンドラ"""
        self._handle_errors(self._process_svg_to_png_conversion)

    def _process_png_to_ico_conversion(self):
        """PNG→ico変換処理"""
        config = load_config()
        downloads_path = config.get('Paths', 'downloads_path')
        output_path = config.get('Paths', 'output_path')
        icon_size = config.getint('Icon', 'icon_size')

        png_file = self._select_file(
            "PNGファイルを選択",
            [("PNG files", "*.png"), ("All files", "*.*")],
            downloads_path
        )

        if not png_file:
            return

        base_name = self._get_base_name(png_file)
        ico_output = os.path.join(output_path, f"{base_name}.ico")

        convert_png_to_ico(png_file, ico_output, icon_size)
        self._open_output_directory(output_path)

    def convert_png_to_ico_handler(self):
        """PNG→ico変換ボタンのハンドラ"""
        self._handle_errors(self._process_png_to_ico_conversion)

    def _process_svg_to_ico_conversion(self):
        """SVG→ico変換処理"""
        config = load_config()
        downloads_path = config.get('Paths', 'downloads_path')
        output_path = config.get('Paths', 'output_path')
        icon_size = config.getint('Icon', 'icon_size')

        svg_file = self._select_file(
            "SVGファイルを選択",
            [("SVG files", "*.svg"), ("All files", "*.*")],
            downloads_path
        )

        if not svg_file:
            return

        base_name = self._get_base_name(svg_file)
        png_output = os.path.join(output_path, f"{base_name}.png")
        ico_output = os.path.join(output_path, f"{base_name}.ico")

        convert_svg_to_png(svg_file, png_output, icon_size)
        convert_png_to_ico(png_output, ico_output, icon_size)
        self._open_output_directory(output_path)

    def convert_svg_to_ico_handler(self):
        """SVG→ico変換ボタンのハンドラ"""
        self._handle_errors(self._process_svg_to_ico_conversion)

    def _process_open_config(self):
        """設定ファイルを開く処理"""
        if os.path.exists(CONFIG_PATH):
            subprocess.Popen(['notepad.exe', CONFIG_PATH])
        else:
            messagebox.showerror("エラー", f"設定ファイルが見つかりません:\n{CONFIG_PATH}")

    def open_config_handler(self):
        """設定ファイルをメモ帳で開く"""
        self._handle_errors(self._process_open_config)
