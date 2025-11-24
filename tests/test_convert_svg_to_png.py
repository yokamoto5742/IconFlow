import os
from unittest.mock import Mock, patch

import pytest

from service.convert_svg_to_png import convert_svg_to_png


class TestConvertSvgToPng:
    """SVG to PNG変換処理のテストクラス"""

    @patch('service.convert_svg_to_png.cairosvg.svg2png')
    def test_convert_svg_to_png_success(self, mock_svg2png):
        """正常系: SVGからPNGへの変換が成功する"""
        input_file = "test.svg"
        output_file = "test.png"

        result = convert_svg_to_png(input_file, output_file)

        mock_svg2png.assert_called_once_with(url=input_file, write_to=output_file)
        assert result == output_file

    @patch('service.convert_svg_to_png.cairosvg.svg2png')
    def test_convert_svg_to_png_file_not_found(self, mock_svg2png):
        """異常系: 入力ファイルが見つからない場合はFileNotFoundErrorが発生"""
        mock_svg2png.side_effect = FileNotFoundError("File not found")
        input_file = "nonexistent.svg"
        output_file = "test.png"

        with pytest.raises(FileNotFoundError):
            convert_svg_to_png(input_file, output_file)

    @patch('service.convert_svg_to_png.cairosvg.svg2png')
    def test_convert_svg_to_png_generic_error(self, mock_svg2png):
        """異常系: 変換中に一般的なエラーが発生"""
        mock_svg2png.side_effect = Exception("Conversion error")
        input_file = "test.svg"
        output_file = "test.png"

        with pytest.raises(Exception) as exc_info:
            convert_svg_to_png(input_file, output_file)
        assert "Conversion error" in str(exc_info.value)

    @patch('service.convert_svg_to_png.cairosvg.svg2png')
    @patch('builtins.print')
    def test_convert_svg_to_png_prints_success_message(self, mock_print, mock_svg2png):
        """正常系: 変換成功時にメッセージが出力される"""
        input_file = "test.svg"
        output_file = "test.png"

        convert_svg_to_png(input_file, output_file)

        mock_print.assert_called_with(f"変換が完了しました: {output_file}")

    @patch('service.convert_svg_to_png.cairosvg.svg2png')
    @patch('builtins.print')
    def test_convert_svg_to_png_prints_file_not_found_error(self, mock_print, mock_svg2png):
        """異常系: FileNotFoundError時にエラーメッセージが出力される"""
        mock_svg2png.side_effect = FileNotFoundError("File not found")
        input_file = "nonexistent.svg"
        output_file = "test.png"

        with pytest.raises(FileNotFoundError):
            convert_svg_to_png(input_file, output_file)

        mock_print.assert_called_with(f"エラー: 入力ファイルが見つかりません: {input_file}")

    @patch('service.convert_svg_to_png.cairosvg.svg2png')
    @patch('builtins.print')
    def test_convert_svg_to_png_prints_generic_error(self, mock_print, mock_svg2png):
        """異常系: 一般的なエラー時にエラーメッセージが出力される"""
        error_msg = "Conversion error"
        mock_svg2png.side_effect = Exception(error_msg)
        input_file = "test.svg"
        output_file = "test.png"

        with pytest.raises(Exception):
            convert_svg_to_png(input_file, output_file)

        mock_print.assert_called_with(f"エラーが発生しました: {error_msg}")

    @patch('service.convert_svg_to_png.cairosvg.svg2png')
    def test_convert_svg_to_png_with_none_input(self, mock_svg2png):
        """異常系: 入力ファイルがNoneの場合"""
        result = convert_svg_to_png(None, "output.png")

        mock_svg2png.assert_called_once_with(url=None, write_to="output.png")
        assert result == "output.png"

    @patch('service.convert_svg_to_png.cairosvg.svg2png')
    def test_convert_svg_to_png_with_none_output(self, mock_svg2png):
        """異常系: 出力ファイルがNoneの場合"""
        result = convert_svg_to_png("input.svg", None)

        mock_svg2png.assert_called_once_with(url="input.svg", write_to=None)
        assert result is None
