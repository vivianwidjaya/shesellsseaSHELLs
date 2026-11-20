import pytest

from app.main import Builtins


def test_echo_without_stdout_redirect(capsys: pytest.CaptureFixture[str]):
    input_str = ["echo", "hello", "world"]
    Builtins(input_str).command()
    output, _err = capsys.readouterr()
    assert "hello world\n" == output


def test_echo_with_spaces(capsys: pytest.CaptureFixture[str]):
    input_str = ["echo", "hello          world"]
    Builtins(input_str).command()
    output, _err = capsys.readouterr()
    assert "hello          world\n" == output


def test_type_is_builtin_single(capsys: pytest.CaptureFixture[str]):
    input_str = ["type", "echo"]
    Builtins(input_str).command()
    output, _err = capsys.readouterr()
    assert "echo is a shell builtin\n" == output


def test_type_is_builtin_multiple(capsys: pytest.CaptureFixture[str]):
    input_str = ["type", "echo", "exit"]
    Builtins(input_str).command()
    output, _err = capsys.readouterr()
    expected_output = """echo is a shell builtin
exit is a shell builtin
"""
    assert output == expected_output
