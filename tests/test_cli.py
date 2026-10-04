"""
Unit tests for CLI commands.
"""

import sys
from unittest.mock import patch
from phantasm_os.cli import main


def test_cli_vfs_list(capsys):
    test_args = ["phantasm-os", "vfs-list", "--dir", "C:\\"]
    with patch.object(sys, "argv", test_args):
        main()
    captured = capsys.readouterr()
    assert "Directory listing for C:\\" in captured.out
    assert "AUTOEXEC.BAT" in captured.out


def test_cli_arg_status(capsys):
    test_args = ["phantasm-os", "arg-status"]
    with patch.object(sys, "argv", test_args):
        main()
    captured = capsys.readouterr()
    assert "PROJECT CHIMERA ARG STATUS" in captured.out
    assert "Stage 1" in captured.out


def test_cli_clippy_chat(capsys):
    test_args = ["phantasm-os", "clippy", "What is Project Chimera?"]
    with patch.object(sys, "argv", test_args):
        main()
    captured = capsys.readouterr()
    assert "[CLIPTRON 95]" in captured.out
    assert "SYSOPS_1995" in captured.out
