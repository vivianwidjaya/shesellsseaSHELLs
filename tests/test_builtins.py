import pytest

from app.main import Builtins


def test_echo_without_stdout_redirect(capsys: pytest.CaptureFixture[str]):
    input_str = ["echo", "hello", "world"]
    Builtins(input_str).command()
    output, err = capsys.readouterr()
    assert output == "hello world\n"
    assert err == ""


def test_echo_with_spaces(capsys: pytest.CaptureFixture[str]):
    input_str = ["echo", "hello          world"]
    Builtins(input_str).command()
    output, _err = capsys.readouterr()
    assert output == "hello          world\n"


def test_type_is_builtin_single(capsys: pytest.CaptureFixture[str]):
    input_str = ["type", "echo"]
    Builtins(input_str).command()
    output, _err = capsys.readouterr()
    assert output == "echo is a shell builtin\n"


def test_type_is_builtin_multiple(capsys: pytest.CaptureFixture[str]):
    input_str = ["type", "echo", "exit"]
    Builtins(input_str).command()
    output, _err = capsys.readouterr()
    expected_output = """echo is a shell builtin
exit is a shell builtin
"""
    assert output == expected_output


def test_type_is_unrecognised(capsys: pytest.CaptureFixture[str]):
    input_str = ["type", "asfgh"]
    Builtins(input_str).command()
    _output, err = capsys.readouterr()
    expected_output = "asfgh: not found\n"
    assert err == expected_output


def test_type_is_executable(capsys: pytest.CaptureFixture[str]):
    input_str = ["type", "ls"]
    Builtins(input_str).command()
    output, _err = capsys.readouterr()
    expected_output = "ls is /usr/bin/ls\n"
    assert output == expected_output
