import os
import tkinter as tk
from unittest.mock import Mock, call, patch

import pytest

from app.main_window import IconFlowMainWindow


class TestIconFlowMainWindow:
    """IconFlowMainWindowのテストクラス"""

    @pytest.fixture
    def mock_root(self):
        """テスト用のルートウィンドウモック"""
        root = Mock(spec=tk.Tk)
        root.tk = Mock()  # tkinter widgets need this attribute
        return root

    @pytest.fixture
    def mock_config(self):
        """テスト用の設定モック"""
        config = Mock()
        config.getint.side_effect = lambda section, key: {
            ('Appearance', 'window_width'): 250,
            ('Appearance', 'window_height'): 300,
            ('Appearance', 'font_size'): 11,
            ('Icon', 'icon_size'): 128,
        }.get((section, key), 0)
        config.get.side_effect = lambda section, key: {
            ('Paths', 'downloads_path'): r'C:\Users\test\Downloads',
            ('Paths', 'output_path'): r'C:\Users\test\output',
        }.get((section, key), '')
        return config

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    def test_init_window_configuration(self, mock_load_config, mock_button, mock_root, mock_config):
        """正常系: ウィンドウの初期化が正しく行われる"""
        mock_load_config.return_value = mock_config

        window = IconFlowMainWindow(mock_root)

        mock_root.title.assert_called_once()
        assert "IconFlow" in mock_root.title.call_args[0][0]
        mock_root.geometry.assert_called_once_with("250x300")
        mock_root.resizable.assert_called_once_with(False, False)

    @patch('app.main_window.load_config')
    @patch('app.main_window.tk.Button')
    def test_init_creates_all_buttons(self, mock_button, mock_load_config, mock_root, mock_config):
        """正常系: 全てのボタンが作成される"""
        mock_load_config.return_value = mock_config

        window = IconFlowMainWindow(mock_root)

        # 5つのボタンが作成されることを確認
        assert mock_button.call_count == 5

        # ボタンのテキストを確認
        button_texts = [call_args[1]['text'] for call_args in mock_button.call_args_list]
        assert "SVGからPNGへ" in button_texts
        assert "PNGからicoへ" in button_texts
        assert "SVGからicoへ" in button_texts
        assert "設定ファイル" in button_texts
        assert "閉じる" in button_texts

    @patch('app.main_window.tk.Button')
    def test_select_file_returns_selected_file(self, mock_button, mock_root):
        """正常系: ファイル選択ダイアログが正しいパスを返す"""
        with patch('app.main_window.load_config'):
            window = IconFlowMainWindow(mock_root)

            with patch('app.main_window.filedialog.askopenfilename', return_value='C:\\test\\file.svg'):
                result = window._select_file("選択", [("SVG", "*.svg")], "C:\\test")

                assert result == 'C:\\test\\file.svg'

    @patch('app.main_window.tk.Button')
    def test_select_file_returns_empty_on_cancel(self, mock_button, mock_root):
        """正常系: ファイル選択をキャンセルすると空文字列を返す"""
        with patch('app.main_window.load_config'):
            window = IconFlowMainWindow(mock_root)

            with patch('app.main_window.filedialog.askopenfilename', return_value=''):
                result = window._select_file("選択", [("SVG", "*.svg")], "C:\\test")

                assert result == ''

    @patch('app.main_window.tk.Button')
    def test_get_base_name_removes_extension(self, mock_button, mock_root):
        """正常系: ファイルのベース名が正しく取得される"""
        with patch('app.main_window.load_config'):
            window = IconFlowMainWindow(mock_root)

            result = window._get_base_name('C:\\test\\file.svg')
            assert result == 'file'

            result = window._get_base_name('C:\\test\\image.png')
            assert result == 'image'

    @patch('app.main_window.tk.Button')
    def test_get_base_name_handles_no_extension(self, mock_button, mock_root):
        """正常系: 拡張子がないファイル名を処理する"""
        with patch('app.main_window.load_config'):
            window = IconFlowMainWindow(mock_root)

            result = window._get_base_name('C:\\test\\file')
            assert result == 'file'

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.os.startfile')
    @patch('app.main_window.os.path.exists')
    def test_open_output_directory_opens_existing_directory(self, mock_exists, mock_startfile, mock_button, mock_root):
        """正常系: 既存のディレクトリを開く"""
        mock_exists.return_value = True
        with patch('app.main_window.load_config'):
            window = IconFlowMainWindow(mock_root)

            window._open_output_directory('C:\\test\\output')

            mock_exists.assert_called_once_with('C:\\test\\output')
            mock_startfile.assert_called_once_with('C:\\test\\output')

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.os.startfile')
    @patch('app.main_window.os.path.exists')
    def test_open_output_directory_does_not_open_nonexistent_directory(self, mock_exists, mock_startfile, mock_button, mock_root):
        """正常系: 存在しないディレクトリは開かない"""
        mock_exists.return_value = False
        with patch('app.main_window.load_config'):
            window = IconFlowMainWindow(mock_root)

            window._open_output_directory('C:\\test\\nonexistent')

            mock_exists.assert_called_once_with('C:\\test\\nonexistent')
            mock_startfile.assert_not_called()

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.messagebox.showerror')
    def test_handle_errors_catches_file_not_found(self, mock_showerror, mock_button, mock_root):
        """異常系: FileNotFoundErrorを捕捉する"""
        with patch('app.main_window.load_config'):
            window = IconFlowMainWindow(mock_root)

            def raise_file_not_found():
                raise FileNotFoundError("Test file not found")

            window._handle_errors(raise_file_not_found)

            mock_showerror.assert_called_once()
            assert "ファイルが見つかりません" in mock_showerror.call_args[0][1]

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.messagebox.showerror')
    def test_handle_errors_catches_generic_exception(self, mock_showerror, mock_button, mock_root):
        """異常系: 一般的な例外を捕捉する"""
        with patch('app.main_window.load_config'):
            window = IconFlowMainWindow(mock_root)

            def raise_generic_error():
                raise Exception("Test error")

            window._handle_errors(raise_generic_error)

            mock_showerror.assert_called_once()
            assert "変換中にエラーが発生しました" in mock_showerror.call_args[0][1]

    @patch('app.main_window.tk.Button')
    def test_handle_errors_executes_successful_function(self, mock_button, mock_root):
        """正常系: エラーがない場合は関数が正常に実行される"""
        with patch('app.main_window.load_config'):
            window = IconFlowMainWindow(mock_root)

            executed = {'value': False}

            def successful_func():
                executed['value'] = True

            window._handle_errors(successful_func)

            assert executed['value'] is True

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    @patch('app.main_window.convert_svg_to_png')
    @patch('app.main_window.filedialog.askopenfilename')
    @patch('app.main_window.os.startfile')
    @patch('app.main_window.os.path.exists')
    def test_process_svg_to_png_conversion_success(
        self, mock_exists, mock_startfile, mock_file_dialog, mock_convert, mock_load_config, mock_button, mock_root, mock_config
    ):
        """正常系: SVG→PNG変換処理が成功する"""
        mock_load_config.return_value = mock_config
        mock_file_dialog.return_value = 'C:\\test\\input.svg'
        mock_exists.return_value = True

        window = IconFlowMainWindow(mock_root)
        window._process_svg_to_png_conversion()

        mock_convert.assert_called_once()
        assert mock_convert.call_args[0][0] == 'C:\\test\\input.svg'
        assert 'input.png' in mock_convert.call_args[0][1]

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    @patch('app.main_window.convert_svg_to_png')
    @patch('app.main_window.filedialog.askopenfilename')
    def test_process_svg_to_png_conversion_cancelled(
        self, mock_file_dialog, mock_convert, mock_load_config, mock_button, mock_root, mock_config
    ):
        """正常系: ファイル選択をキャンセルした場合は変換しない"""
        mock_load_config.return_value = mock_config
        mock_file_dialog.return_value = ''

        window = IconFlowMainWindow(mock_root)
        window._process_svg_to_png_conversion()

        mock_convert.assert_not_called()

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    @patch('app.main_window.convert_png_to_ico')
    @patch('app.main_window.filedialog.askopenfilename')
    @patch('app.main_window.os.startfile')
    @patch('app.main_window.os.path.exists')
    def test_process_png_to_ico_conversion_success(
        self, mock_exists, mock_startfile, mock_file_dialog, mock_convert, mock_load_config, mock_button, mock_root, mock_config
    ):
        """正常系: PNG→ICO変換処理が成功する"""
        mock_load_config.return_value = mock_config
        mock_file_dialog.return_value = 'C:\\test\\input.png'
        mock_exists.return_value = True

        window = IconFlowMainWindow(mock_root)
        window._process_png_to_ico_conversion()

        mock_convert.assert_called_once()
        assert mock_convert.call_args[0][0] == 'C:\\test\\input.png'
        assert 'input.ico' in mock_convert.call_args[0][1]

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    @patch('app.main_window.convert_png_to_ico')
    @patch('app.main_window.filedialog.askopenfilename')
    def test_process_png_to_ico_conversion_cancelled(
        self, mock_file_dialog, mock_convert, mock_load_config, mock_button, mock_root, mock_config
    ):
        """正常系: ファイル選択をキャンセルした場合は変換しない"""
        mock_load_config.return_value = mock_config
        mock_file_dialog.return_value = ''

        window = IconFlowMainWindow(mock_root)
        window._process_png_to_ico_conversion()

        mock_convert.assert_not_called()

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    @patch('app.main_window.convert_svg_to_png')
    @patch('app.main_window.convert_png_to_ico')
    @patch('app.main_window.filedialog.askopenfilename')
    @patch('app.main_window.os.startfile')
    @patch('app.main_window.os.path.exists')
    def test_process_svg_to_ico_conversion_success(
        self, mock_exists, mock_startfile, mock_file_dialog, mock_convert_ico,
        mock_convert_png, mock_load_config, mock_button, mock_root, mock_config
    ):
        """正常系: SVG→ICO変換処理が成功する"""
        mock_load_config.return_value = mock_config
        mock_file_dialog.return_value = 'C:\\test\\input.svg'
        mock_exists.return_value = True

        window = IconFlowMainWindow(mock_root)
        window._process_svg_to_ico_conversion()

        mock_convert_png.assert_called_once()
        mock_convert_ico.assert_called_once()
        assert 'input.png' in mock_convert_png.call_args[0][1]
        assert 'input.ico' in mock_convert_ico.call_args[0][1]

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    @patch('app.main_window.convert_svg_to_png')
    @patch('app.main_window.convert_png_to_ico')
    @patch('app.main_window.filedialog.askopenfilename')
    def test_process_svg_to_ico_conversion_cancelled(
        self, mock_file_dialog, mock_convert_ico, mock_convert_png, mock_load_config, mock_button, mock_root, mock_config
    ):
        """正常系: ファイル選択をキャンセルした場合は変換しない"""
        mock_load_config.return_value = mock_config
        mock_file_dialog.return_value = ''

        window = IconFlowMainWindow(mock_root)
        window._process_svg_to_ico_conversion()

        mock_convert_png.assert_not_called()
        mock_convert_ico.assert_not_called()

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    @patch('app.main_window.subprocess.Popen')
    @patch('app.main_window.os.path.exists')
    @patch('app.main_window.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_process_open_config_success(self, mock_exists, mock_popen, mock_load_config, mock_button, mock_root, mock_config):
        """正常系: 設定ファイルをメモ帳で開く"""
        mock_load_config.return_value = mock_config
        mock_exists.return_value = True

        window = IconFlowMainWindow(mock_root)
        window._process_open_config()

        mock_popen.assert_called_once_with(['notepad.exe', 'C:\\test\\config.ini'])

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    @patch('app.main_window.messagebox.showerror')
    @patch('app.main_window.os.path.exists')
    @patch('app.main_window.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_process_open_config_file_not_found(self, mock_exists, mock_showerror, mock_load_config, mock_button, mock_root, mock_config):
        """異常系: 設定ファイルが見つからない場合"""
        mock_load_config.return_value = mock_config
        mock_exists.return_value = False

        window = IconFlowMainWindow(mock_root)
        window._process_open_config()

        mock_showerror.assert_called_once()
        assert "設定ファイルが見つかりません" in mock_showerror.call_args[0][1]

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    @patch('app.main_window.messagebox.showerror')
    def test_convert_svg_to_png_handler_calls_handle_errors(self, mock_showerror, mock_load_config, mock_button, mock_root, mock_config):
        """正常系: ハンドラがエラーハンドリングを使用する"""
        mock_load_config.return_value = mock_config

        window = IconFlowMainWindow(mock_root)

        # _process_svg_to_png_conversionをモック化してエラーを発生させる
        with patch.object(window, '_process_svg_to_png_conversion', side_effect=Exception("Test error")):
            window.convert_svg_to_png_handler()

        mock_showerror.assert_called_once()

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    @patch('app.main_window.messagebox.showerror')
    def test_convert_png_to_ico_handler_calls_handle_errors(self, mock_showerror, mock_load_config, mock_button, mock_root, mock_config):
        """正常系: ハンドラがエラーハンドリングを使用する"""
        mock_load_config.return_value = mock_config

        window = IconFlowMainWindow(mock_root)

        with patch.object(window, '_process_png_to_ico_conversion', side_effect=Exception("Test error")):
            window.convert_png_to_ico_handler()

        mock_showerror.assert_called_once()

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    @patch('app.main_window.messagebox.showerror')
    def test_convert_svg_to_ico_handler_calls_handle_errors(self, mock_showerror, mock_load_config, mock_button, mock_root, mock_config):
        """正常系: ハンドラがエラーハンドリングを使用する"""
        mock_load_config.return_value = mock_config

        window = IconFlowMainWindow(mock_root)

        with patch.object(window, '_process_svg_to_ico_conversion', side_effect=Exception("Test error")):
            window.convert_svg_to_ico_handler()

        mock_showerror.assert_called_once()

    @patch('app.main_window.tk.Button')
    @patch('app.main_window.load_config')
    @patch('app.main_window.messagebox.showerror')
    def test_open_config_handler_calls_handle_errors(self, mock_showerror, mock_load_config, mock_button, mock_root, mock_config):
        """正常系: ハンドラがエラーハンドリングを使用する"""
        mock_load_config.return_value = mock_config

        window = IconFlowMainWindow(mock_root)

        with patch.object(window, '_process_open_config', side_effect=Exception("Test error")):
            window.open_config_handler()

        mock_showerror.assert_called_once()
