"""(d) Config loading (defaults, TOML file, env override) + logging setup +
config pass-through rules of the CLI."""
import logging
import os

import pytest

from koor import __version__, cli, config
from koor.logging_setup import setup_logging, LOGGER_NAME


def test_defaults_follow_checkout_layout(project_dir, root_dir):
    cfg = config.load_config(env={}, cwd=str(os.devnull))
    assert cfg.config_file == ""
    assert os.path.normcase(cfg.root) == os.path.normcase(root_dir)
    assert os.path.normcase(cfg.output_dir) == os.path.normcase(os.path.join(root_dir, "output"))
    assert os.path.normcase(cfg.splits_dir) == os.path.normcase(os.path.join(root_dir, "splits"))
    assert os.path.normcase(cfg.report_dir) == os.path.normcase(
        os.path.join(project_dir, "precision_report"))
    assert cfg.log_level == "INFO" and cfg.names_file == ""
    assert all(v == "default" for v in cfg.sources.values())
    assert not cfg.explicit("names_file")


def test_file_values_and_derived_defaults(tmp_path):
    data = tmp_path / "data"
    f = tmp_path / "koor.toml"
    f.write_text('[paths]\nroot = "%s"\nnames_file = "predictions/subset.txt"\n'
                 '[logging]\nlevel = "debug"\n' % data.as_posix(), encoding="utf-8")
    cfg = config.load_config(path=str(f), env={})
    assert os.path.normcase(cfg.root) == os.path.normcase(str(data))
    # unspecified paths derive from the configured root
    assert os.path.normcase(cfg.output_dir) == os.path.normcase(str(data / "output"))
    # relative paths resolve against the config file's directory
    assert os.path.normcase(cfg.names_file) == os.path.normcase(
        str(tmp_path / "predictions" / "subset.txt"))
    assert cfg.explicit("root") and cfg.explicit("names_file")
    assert not cfg.explicit("output_dir")
    assert cfg.log_level == "DEBUG"


def test_env_overrides_file(tmp_path):
    f = tmp_path / "koor.toml"
    f.write_text('[paths]\nroot = "%s"\noutput_dir = "%s"\n'
                 % ((tmp_path / "from_file").as_posix(), (tmp_path / "out_file").as_posix()),
                 encoding="utf-8")
    env = {"KOOR_ROOT": str(tmp_path / "from_env"),
           "KOOR_LOG_LEVEL": "warning", "KOOR_NAMES_FILE": str(tmp_path / "n.txt")}
    cfg = config.load_config(path=str(f), env=env)
    assert os.path.normcase(cfg.root) == os.path.normcase(str(tmp_path / "from_env"))
    assert cfg.sources["root"] == "env"
    assert cfg.sources["output_dir"] == "file"          # file value kept where env is silent
    assert os.path.normcase(cfg.output_dir) == os.path.normcase(str(tmp_path / "out_file"))
    # splits_dir was set nowhere -> derived from the *env* root
    assert os.path.normcase(cfg.splits_dir) == os.path.normcase(
        str(tmp_path / "from_env" / "splits"))
    assert cfg.log_level == "WARNING" and cfg.sources["log_level"] == "env"
    assert cfg.explicit("names_file")


def test_koor_config_env_selects_file(tmp_path):
    f = tmp_path / "custom.toml"
    f.write_text('[paths]\nroot = "%s"\n' % (tmp_path / "r").as_posix(), encoding="utf-8")
    cfg = config.load_config(env={"KOOR_CONFIG": str(f)}, cwd=str(tmp_path))
    assert os.path.normcase(cfg.config_file) == os.path.normcase(str(f))
    assert cfg.sources["root"] == "file"
    with pytest.raises(FileNotFoundError):
        config.load_config(path=str(tmp_path / "nope.toml"), env={})


def test_cwd_koor_toml_is_found(tmp_path):
    (tmp_path / "koor.toml").write_text('[logging]\nlevel = "error"\n', encoding="utf-8")
    cfg = config.load_config(env={}, cwd=str(tmp_path))
    assert cfg.log_level == "ERROR" and cfg.sources["log_level"] == "file"


def test_example_config_parses_with_both_parsers(project_dir):
    example = os.path.join(project_dir, "koor.example.toml")
    assert os.path.isfile(example)
    text = open(example, encoding="utf-8").read()
    mini = config._parse_toml_minimal(text)
    assert mini["paths"]["root"].replace("\\", "/") == "E:/3005/data"
    assert mini["logging"]["level"] == "INFO"
    try:
        import tomllib
    except ImportError:
        tomllib = pytest.importorskip("tomli")
    assert tomllib.loads(text) == mini
    cfg = config.load_config(path=example, env={})
    assert os.path.normcase(cfg.output_dir) == os.path.normcase(r"E:\3005\data\output")
    assert os.path.normcase(cfg.splits_dir) == os.path.normcase(r"E:\3005\data\splits")
    assert cfg.explicit("root") and not cfg.explicit("names_file")


def test_minimal_parser_types():
    d = config._parse_toml_minimal(
        '# c\n[a]\nx = 1\ny = 2.5\nz = true\ns = "q\\"t"  # trailing\n[b.c]\nk = \'lit\'\n')
    assert d == {"a": {"x": 1, "y": 2.5, "z": True, "s": 'q"t'}, "b.c": {"k": "lit"}}
    with pytest.raises(ValueError):
        config._parse_toml_minimal("garbage line\n")


def test_config_subcommand_prints_effective_values(capsys):
    assert cli.main(["config"]) == 0
    out = capsys.readouterr().out
    assert "root" in out and "output_dir" in out and "KOOR_ROOT" in out


# --- pass-through: only explicit keys, only options the script already has ---
def _cfg(**explicit):
    c = config.load_config(env={}, cwd=str(os.devnull))
    for k, v in explicit.items():
        setattr(c, k, v)
        c.sources[k] = "file"
    return c


def test_passthrough_only_when_explicit_and_absent(caplog):
    log = logging.getLogger("test")
    cmd = cli.BY_NAME["eval-predictions"]
    # not configured -> argv untouched (script default unchanged)
    assert cli.apply_config_passthrough(cmd, ["--self-test"], _cfg(), log) == ["--self-test"]
    # configured -> injected
    c = _cfg(names_file=r"E:\x\subset.txt")
    assert cli.apply_config_passthrough(cmd, ["--self-test"], c, log) == \
        ["--names-file", r"E:\x\subset.txt", "--self-test"]
    # given on the command line -> command line wins
    argv = ["--names-file", "mine.txt", "--limit", "3"]
    assert cli.apply_config_passthrough(cmd, argv, c, log) == argv
    assert cli.apply_config_passthrough(cmd, ["--names-file=mine.txt"], c, log) == \
        ["--names-file=mine.txt"]
    # commands without a path option never get anything injected
    for name in ("augment", "export", "geometry", "eval-precision", "quantization",
                 "retrieval", "score"):
        assert cli.apply_config_passthrough(cli.BY_NAME[name], ["a"], c, log) == ["a"]


# --- logging ---------------------------------------------------------------
def test_setup_logging_console_and_file(tmp_path, capsys):
    logfile = tmp_path / "logs" / "koor.log"
    log = setup_logging("DEBUG", str(logfile))
    assert log.name == LOGGER_NAME and log.level == logging.DEBUG
    log.info("hello from test")
    for h in log.handlers:
        h.flush()
    assert "hello from test" in capsys.readouterr().err
    assert "hello from test" in logfile.read_text(encoding="utf-8")
    # re-configuring replaces handlers instead of stacking them
    log2 = setup_logging("INFO")
    assert log2 is log and len(log.handlers) == 1
    with pytest.raises(ValueError):
        setup_logging("NOT_A_LEVEL")


def test_version_matches_pyproject(project_dir):
    text = open(os.path.join(project_dir, "pyproject.toml"), encoding="utf-8").read()
    assert 'version = "%s"' % __version__ in text
    assert 'name = "complexcad-koor"' in text


def test_transform_subcommand_end_to_end(run_koor, box_program, tmp_path):
    """`koor transform` (runpy dispatch of koor_transform.__main__) with logging
    to a file: the quantised program comes back on stdout."""
    logfile = tmp_path / "cli.log"
    cp = run_koor("--log-file", str(logfile), "transform", input=box_program)
    assert cp.returncode == 0, cp.stderr
    assert "box(2000, 1000, 500)" in cp.stdout.replace("width, depth, height", "")\
        or ("2000" in cp.stdout and "1000" in cp.stdout and "500" in cp.stdout)
    assert "# stats:" in cp.stderr                       # the script's own stderr line
    assert "run transform" in logfile.read_text(encoding="utf-8")
