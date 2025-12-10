from unittest.mock import Mock, call, patch

import pytest
from PIL import Image

from service.convert_png_to_ico import convert_png_to_ico


class TestConvertPngToIco:
    """PNG to ICO変換処理のテストクラス"""

    @patch('service.convert_png_to_ico.Image.open')
    @patch('builtins.print')
    def test_convert_png_to_ico_success(self, mock_print, mock_image_open):
        """正常系: PNGからICOへの変換が成功する"""
        mock_image = Mock(spec=Image.Image)
        mock_resized_image = Mock(spec=Image.Image)
        mock_image_open.return_value = mock_image
        mock_image.resize.return_value = mock_resized_image

        png_path = "test.png"
        ico_path = "test.ico"
        size = 128

        convert_png_to_ico(png_path, ico_path, size)

        mock_image_open.assert_called_once_with(png_path)
        mock_image.resize.assert_called_once_with((size, size), Image.Resampling.LANCZOS)
        mock_resized_image.save.assert_called_once_with(ico_path, format='ICO', sizes=[(size, size)])
        assert mock_print.call_count == 4

    @patch('service.convert_png_to_ico.Image.open')
    def test_convert_png_to_ico_default_size(self, mock_image_open):
        """正常系: デフォルトサイズ128で変換される"""
        mock_image = Mock(spec=Image.Image)
        mock_resized_image = Mock(spec=Image.Image)
        mock_image_open.return_value = mock_image
        mock_image.resize.return_value = mock_resized_image

        convert_png_to_ico("test.png", "test.ico")

        mock_image.resize.assert_called_once_with((128, 128), Image.Resampling.LANCZOS)

    @patch('service.convert_png_to_ico.Image.open')
    def test_convert_png_to_ico_custom_size(self, mock_image_open):
        """正常系: カスタムサイズで変換される"""
        mock_image = Mock(spec=Image.Image)
        mock_resized_image = Mock(spec=Image.Image)
        mock_image_open.return_value = mock_image
        mock_image.resize.return_value = mock_resized_image

        custom_size = 256
        convert_png_to_ico("test.png", "test.ico", custom_size)

        mock_image.resize.assert_called_once_with((custom_size, custom_size), Image.Resampling.LANCZOS)

    @patch('service.convert_png_to_ico.Image.open')
    def test_convert_png_to_ico_file_not_found(self, mock_image_open):
        """異常系: 入力ファイルが見つからない場合はFileNotFoundErrorが発生"""
        mock_image_open.side_effect = FileNotFoundError("File not found")

        with pytest.raises(FileNotFoundError):
            convert_png_to_ico("nonexistent.png", "test.ico")

    @patch('service.convert_png_to_ico.Image.open')
    def test_convert_png_to_ico_invalid_image(self, mock_image_open):
        """異常系: 無効な画像ファイルの場合はエラーが発生"""
        mock_image_open.side_effect = Exception("Cannot identify image file")

        with pytest.raises(Exception):
            convert_png_to_ico("invalid.png", "test.ico")

    @patch('service.convert_png_to_ico.Image.open')
    def test_convert_png_to_ico_save_error(self, mock_image_open):
        """異常系: 保存中にエラーが発生"""
        mock_image = Mock(spec=Image.Image)
        mock_resized_image = Mock(spec=Image.Image)
        mock_image_open.return_value = mock_image
        mock_image.resize.return_value = mock_resized_image
        mock_resized_image.save.side_effect = IOError("Cannot write file")

        with pytest.raises(IOError):
            convert_png_to_ico("test.png", "test.ico")

    @patch('service.convert_png_to_ico.Image.open')
    def test_convert_png_to_ico_zero_size(self, mock_image_open):
        """異常系: サイズが0の場合"""
        mock_image = Mock(spec=Image.Image)
        mock_resized_image = Mock(spec=Image.Image)
        mock_image_open.return_value = mock_image
        mock_image.resize.return_value = mock_resized_image

        convert_png_to_ico("test.png", "test.ico", 0)

        mock_image.resize.assert_called_once_with((0, 0), Image.Resampling.LANCZOS)

    @patch('service.convert_png_to_ico.Image.open')
    def test_convert_png_to_ico_negative_size(self, mock_image_open):
        """異常系: サイズが負の値の場合"""
        mock_image = Mock(spec=Image.Image)
        mock_resized_image = Mock(spec=Image.Image)
        mock_image_open.return_value = mock_image
        mock_image.resize.return_value = mock_resized_image

        convert_png_to_ico("test.png", "test.ico", -100)

        mock_image.resize.assert_called_once_with((-100, -100), Image.Resampling.LANCZOS)

    @patch('service.convert_png_to_ico.Image.open')
    def test_convert_png_to_ico_large_size(self, mock_image_open):
        """正常系: 大きいサイズでの変換"""
        mock_image = Mock(spec=Image.Image)
        mock_resized_image = Mock(spec=Image.Image)
        mock_image_open.return_value = mock_image
        mock_image.resize.return_value = mock_resized_image

        large_size = 1024
        convert_png_to_ico("test.png", "test.ico", large_size)

        mock_image.resize.assert_called_once_with((large_size, large_size), Image.Resampling.LANCZOS)

    @patch('service.convert_png_to_ico.Image.open')
    def test_convert_png_to_ico_uses_lanczos_resampling(self, mock_image_open):
        """正常系: LANCZOSリサンプリングが使用される"""
        mock_image = Mock(spec=Image.Image)
        mock_resized_image = Mock(spec=Image.Image)
        mock_image_open.return_value = mock_image
        mock_image.resize.return_value = mock_resized_image

        convert_png_to_ico("test.png", "test.ico")

        # LANCZOSリサンプリングが使用されていることを確認
        call_args = mock_image.resize.call_args
        # 2番目の引数としてLANCZOSが渡されていることを確認
        assert len(call_args[0]) >= 2
        assert call_args[0][1] == Image.Resampling.LANCZOS
