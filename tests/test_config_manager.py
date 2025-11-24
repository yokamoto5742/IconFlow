import configparser
import os
import sys
from unittest.mock import Mock, mock_open, patch

import pytest

from utils.config_manager import CONFIG_PATH, get_config_path, load_config, save_config


class TestGetConfigPath:
    """get_config_path関数のテストクラス"""

    @patch('sys.frozen', True, create=True)
    @patch('sys._MEIPASS', 'C:\\frozen\\path', create=True)
    def test_get_config_path_frozen_executable(self):
        """正常系: PyInstallerでビルドされた実行ファイルの場合"""
        with patch('utils.config_manager.sys') as mock_sys:
            mock_sys.frozen = True
            mock_sys._MEIPASS = 'C:\\frozen\\path'

            path = get_config_path()

            assert path == 'C:\\frozen\\path\\config.ini'

    @patch('sys.frozen', False, create=True)
    @patch('utils.config_manager.os.path.dirname')
    def test_get_config_path_normal_script(self, mock_dirname):
        """正常系: 通常のPythonスクリプトとして実行される場合"""
        mock_dirname.return_value = 'C:\\project\\utils'

        with patch('utils.config_manager.sys') as mock_sys:
            mock_sys.frozen = False
            delattr(mock_sys, '_MEIPASS')

            path = get_config_path()

            assert path == 'C:\\project\\utils\\config.ini'

    def test_get_config_path_returns_string(self):
        """正常系: 戻り値が文字列である"""
        path = get_config_path()
        assert isinstance(path, str)

    def test_get_config_path_ends_with_config_ini(self):
        """正常系: パスがconfig.iniで終わる"""
        path = get_config_path()
        assert path.endswith('config.ini')


class TestLoadConfig:
    """load_config関数のテストクラス"""

    @patch('builtins.open', new_callable=mock_open, read_data='[Section]\nkey=value\n')
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_load_config_success(self, mock_file):
        """正常系: 設定ファイルが正常に読み込まれる"""
        config = load_config()

        assert isinstance(config, configparser.ConfigParser)
        mock_file.assert_called_once_with('C:\\test\\config.ini', encoding='utf-8')

    @patch('builtins.open', side_effect=FileNotFoundError())
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\nonexistent.ini')
    def test_load_config_file_not_found(self, mock_file):
        """異常系: 設定ファイルが見つからない場合"""
        with pytest.raises(FileNotFoundError):
            load_config()

    @patch('builtins.open', new_callable=mock_open, read_data='[Invalid')
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_load_config_parse_error(self, mock_file):
        """異常系: 設定ファイルの解析エラー"""
        with pytest.raises(configparser.Error):
            load_config()

    @patch('builtins.open', new_callable=mock_open, read_data='[Appearance]\nfont_size=11\n')
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_load_config_returns_correct_values(self, mock_file):
        """正常系: 設定値が正しく読み込まれる"""
        config = load_config()

        assert config.has_section('Appearance')
        assert config.get('Appearance', 'font_size') == '11'

    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_load_config_empty_file(self, mock_file):
        """正常系: 空の設定ファイル"""
        config = load_config()

        assert isinstance(config, configparser.ConfigParser)
        assert len(config.sections()) == 0

    @patch('builtins.open', side_effect=PermissionError())
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_load_config_permission_error(self, mock_file):
        """異常系: ファイル読み込み権限エラー"""
        with pytest.raises(PermissionError):
            load_config()

    @patch('builtins.print')
    @patch('builtins.open', side_effect=FileNotFoundError())
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_load_config_prints_file_not_found_error(self, mock_file, mock_print):
        """異常系: FileNotFoundError時にエラーメッセージが出力される"""
        with pytest.raises(FileNotFoundError):
            load_config()

        mock_print.assert_called()
        assert "設定ファイルが見つかりません" in mock_print.call_args[0][0]

    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open, read_data='[Invalid')
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_load_config_prints_parse_error(self, mock_file, mock_print):
        """異常系: 解析エラー時にエラーメッセージが出力される"""
        with pytest.raises(configparser.Error):
            load_config()

        mock_print.assert_called()
        assert "設定ファイルの解析中にエラーが発生しました" in mock_print.call_args[0][0]


class TestSaveConfig:
    """save_config関数のテストクラス"""

    @patch('builtins.open', new_callable=mock_open)
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_save_config_success(self, mock_file):
        """正常系: 設定ファイルが正常に保存される"""
        config = configparser.ConfigParser()
        config.add_section('Test')
        config.set('Test', 'key', 'value')

        save_config(config)

        mock_file.assert_called_once_with('C:\\test\\config.ini', 'w', encoding='utf-8')
        handle = mock_file()
        handle.write.assert_called()

    @patch('builtins.open', side_effect=IOError('Write error'))
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_save_config_io_error(self, mock_file):
        """異常系: ファイル書き込みエラー"""
        config = configparser.ConfigParser()

        with pytest.raises(IOError):
            save_config(config)

    @patch('builtins.open', side_effect=PermissionError())
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_save_config_permission_error(self, mock_file):
        """異常系: ファイル書き込み権限エラー"""
        config = configparser.ConfigParser()

        with pytest.raises(PermissionError):
            save_config(config)

    @patch('builtins.print')
    @patch('builtins.open', side_effect=IOError('Write error'))
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_save_config_prints_io_error(self, mock_file, mock_print):
        """異常系: IOError時にエラーメッセージが出力される"""
        config = configparser.ConfigParser()

        with pytest.raises(IOError):
            save_config(config)

        mock_print.assert_called()
        assert "設定ファイルの保存中にエラーが発生しました" in mock_print.call_args[0][0]

    @patch('builtins.open', new_callable=mock_open)
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_save_config_empty_config(self, mock_file):
        """正常系: 空の設定を保存する"""
        config = configparser.ConfigParser()

        save_config(config)

        mock_file.assert_called_once_with('C:\\test\\config.ini', 'w', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    @patch('utils.config_manager.CONFIG_PATH', 'C:\\test\\config.ini')
    def test_save_config_multiple_sections(self, mock_file):
        """正常系: 複数のセクションを持つ設定を保存する"""
        config = configparser.ConfigParser()
        config.add_section('Section1')
        config.set('Section1', 'key1', 'value1')
        config.add_section('Section2')
        config.set('Section2', 'key2', 'value2')

        save_config(config)

        mock_file.assert_called_once_with('C:\\test\\config.ini', 'w', encoding='utf-8')


class TestConfigPath:
    """CONFIG_PATH定数のテストクラス"""

    def test_config_path_is_string(self):
        """正常系: CONFIG_PATHが文字列である"""
        assert isinstance(CONFIG_PATH, str)

    def test_config_path_not_empty(self):
        """正常系: CONFIG_PATHが空でない"""
        assert len(CONFIG_PATH) > 0

    def test_config_path_contains_config_ini(self):
        """正常系: CONFIG_PATHにconfig.iniが含まれる"""
        assert 'config.ini' in CONFIG_PATH
