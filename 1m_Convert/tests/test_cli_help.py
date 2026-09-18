"""(a) ``koor --help`` and ``koor <subcommand> --help`` for every subcommand."""
import os
import shutil
import subprocess
import sys

import pytest

from koor import __version__, cli

REQUIRED = ["augment", "export", "geometry", "eval-precision", "eval-predictions",
            "retrieval", "quantization", "score"]


def test_required_subcommands_are_registered():
    for name in REQUIRED:
        assert name in cli.BY_NAME, name
    # every registered command points at an existing script in koor/
    for c in cli.COMMANDS:
        assert os.path.isfile(c.script), c.script


def test_top_level_help(capsys):
    with pytest.raises(SystemExit) as ex:
        cli.main(["--help"])
    assert ex.value.code == 0
    out = capsys.readouterr().out
    assert "usage: koor" in out
    for name in REQUIRED:
        assert name in out


def test_no_command_prints_help(capsys):
    assert cli.main([]) == 0
    assert "usage: koor" in capsys.readouterr().out


def test_version(capsys):
    with pytest.raises(SystemExit):
        cli.main(["--version"])
    assert __version__ in capsys.readouterr().out


@pytest.mark.parametrize("name", [c.name for c in cli.COMMANDS])
def test_subcommand_help(name, capsys):
    cmd = cli.BY_NAME[name]
    assert cli.main([name, "--help"]) == 0
    out = capsys.readouterr().out
    assert os.path.basename(cmd.script) in out          # names the script it wraps
    assert cmd.summary.split("  ")[0] in out
    if cmd.argparse:
        # either the script's own argparse usage, or a note that an optional
        # dependency (e.g. pyarrow for the 1M chain) is missing in this env
        assert "usage:" in out or "unavailable in this environment" in out


@pytest.mark.parametrize("name", REQUIRED)
def test_subcommand_dash_h(name, capsys):
    assert cli.main([name, "-h"]) == 0
    assert os.path.basename(cli.BY_NAME[name].script) in capsys.readouterr().out


def test_argparse_scripts_show_their_own_options(capsys):
    # eval_precision.py defines --jobs/--limit/--resume itself; the CLI must
    # surface that help unchanged (proves argv is handed through verbatim).
    cli.main(["eval-precision", "--help"])
    out = capsys.readouterr().out
    assert "--jobs" in out and "--resume" in out and "eval_precision.py" in out
    cli.main(["quantization", "--help"])
    assert "--levels" in capsys.readouterr().out


def test_unknown_command_is_rejected(capsys):
    with pytest.raises(SystemExit) as ex:
        cli.main(["no-such-command"])
    assert ex.value.code == 2


def test_python_m_koor_help(run_koor):
    cp = run_koor("--help")
    assert cp.returncode == 0, cp.stderr
    assert "usage: koor" in cp.stdout and "eval-precision" in cp.stdout


def test_console_script_if_installed():
    """`koor --help` through the console entry point created by pip."""
    exe = shutil.which("koor") or os.path.join(
        sys.prefix, "Scripts" if os.name == "nt" else "bin",
        "koor.exe" if os.name == "nt" else "koor")
    if not os.path.isfile(exe):
        pytest.skip("complexcad-koor not pip-installed in this interpreter")
    cp = subprocess.run([exe, "--help"], capture_output=True, text=True,
                        encoding="utf-8", timeout=120,
                        env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    assert cp.returncode == 0, cp.stderr
    assert "usage: koor" in cp.stdout
