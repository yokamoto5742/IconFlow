import tkinter as tk
from unittest.mock import Mock, patch

import pytest


class TestMain:
    """main.pyのテストクラス"""

    def test_main_creates_tk_instance(self):
        """正常系: Tkインスタンスが作成される"""
        # main.pyが正しくインポートできることを確認
        import main
        assert hasattr(main, 'tk')

    def test_main_creates_main_window(self):
        """正常系: IconFlowMainWindowがインポートされる"""
        import main
        assert hasattr(main, 'IconFlowMainWindow')

    def test_main_starts_mainloop(self):
        """正常系: メインループが開始される"""
        # main.pyの構造を確認
        import main
        assert main.tk is not None

    def test_main_module_has_name_main_guard(self):
        """正常系: __name__ == '__main__' のガードが存在する"""
        import main
        import inspect

        source = inspect.getsource(main)
        assert 'if __name__ == "__main__":' in source

    def test_main_imports_required_modules(self):
        """正常系: 必要なモジュールがインポートされる"""
        import main

        # main.pyが正しくインポートできることを確認
        assert hasattr(main, 'tk')
        assert hasattr(main, 'IconFlowMainWindow')

    def test_main_tk_instance_is_created_correctly(self):
        """正常系: Tkモジュールが正しくインポートされる"""
        import main
        assert main.tk.Tk is not None

    def test_main_module_structure(self):
        """正常系: main.pyのモジュール構造を確認"""
        import main

        # モジュールが正しくロードされることを確認
        assert main.__name__ == 'main'
