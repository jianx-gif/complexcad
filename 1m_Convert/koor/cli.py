"""``koor`` -- command-line entry point for the thesis toolchain.

Every subcommand dispatches to one of the unchanged scripts in this package:
the script's own ``main()`` is called in-process with ``sys.argv`` set to
``[<script path>, *args]`` (or, for scripts that only have an
``if __name__ == "__main__"`` block, the module is re-executed with
:func:`runpy.run_module`). The scripts therefore run the very same code path
as ``python koor/<script>.py args...``; the CLI only adds argument routing,
optional configuration (:mod:`koor.config`) and logging
(:mod:`koor.logging_setup`).

    koor --help                       list subcommands
    koor <cmd> --help                 script docstring + the script's own options
    koor eval-precision --jobs 8      == python koor/eval_precision.py --jobs 8
    koor geometry --all 20            == python koor/build_koor_geometry.py --all 20
    koor config                       show the effective configuration
"""
import argparse
import ast
import importlib
import os
import runpy
import sys
import time
from dataclasses import dataclass

from . import __version__
from .config import load_config
from .logging_setup import setup_logging

HERE = os.path.dirname(os.path.abspath(__file__))


@dataclass(frozen=True)
class Command:
    name: str            # subcommand
    module: str          # koor.<module>
    summary: str         # one line for `koor --help`
    mode: str = "main"   # "main": call module.main(); "runpy": re-run module as __main__
    argparse: bool = False   # script parses its args with argparse (own --help)
    # script option -> config field, forwarded only when the field is explicit
    passthrough: tuple = ()

    @property
    def script(self):
        return os.path.join(HERE, self.module + ".py")


COMMANDS = [
    # --- 落地 / 全模态 ------------------------------------------------------
    Command("augment", "augment_koor",
            "给 koor_geometry/<uuid>/ 批量补点云/BREP/文本  [N]"),
    Command("export", "export_to_output",
            "把转换件按原始代码落地到 output_koor/ 布局  [N]"),
    Command("geometry", "build_koor_geometry",
            "量化代码 -> STEP/STL/工程图/三模态 -> koor_geometry/  <uuid>... | --all [N]"),
    Command("extract", "extract_converted_py",
            "从 parquet 提取量化代码到 converted_py/<uuid>/  [N]"),
    # --- 评估 ---------------------------------------------------------------
    Command("eval-precision", "eval_precision",
            "任务4 建模精度评估 (output/ 全量) -> precision_report/metrics.jsonl",
            argparse=True),
    Command("eval-predictions", "eval_predictions",
            "Ch6 评测 harness: 预测代码 vs GT (validity/CD/F/op recall)",
            argparse=True, passthrough=(("--names-file", "names_file"),)),
    Command("retrieval", "retrieval_baseline",
            "非学习检索基线 -> predictions/retrieval/<uuid>.py", argparse=True),
    Command("quantization", "quantization_loss",
            "DeepCAD 式 256 级参数量化损失实验", argparse=True),
    Command("score", "score_safe",
            "防崩评分驱动 (子进程+硬超时)  <method> <names_file>", argparse=True),
    Command("score-one", "score_one",
            "隔离评分单个预测 (通常由 score 调用)  <uuid> <pred_path>"),
    Command("report", "build_report",
            "从 metrics.jsonl 汇总精度报告 + 图表"),
    Command("adapt-cadrecode", "adapt_cadrecode",
            "点云适配成 CAD-Recode 输入", argparse=True,
            passthrough=(("--names-file", "names_file"),)),
    # --- 1M 转换链 ------------------------------------------------------------
    Command("transform", "koor_transform",
            "AST 语义缩放单个程序 (stdin 或 <file>) -> stdout", mode="runpy"),
    Command("convert", "convert_1m",
            "1M 全量转换驱动 (HF parquet -> koor_1m/<split>/)", argparse=True,
            passthrough=(("--outdir", "convert_outdir"),)),
    Command("recover", "recover_1m",
            "恢复 pass: 长超时救回失败项", argparse=True,
            passthrough=(("--dir", "convert_train_dir"),)),
    Command("peek", "peek_1m",
            "查看转换进度 + 抽样", argparse=True,
            passthrough=(("--dir", "convert_train_dir"),)),
    Command("verify-recover", "verify_recover",
            "验证量化代码可无损还原  [N]"),
    Command("verify-fast", "verify_fast",
            "抽样校验几何落在 [1,10000]  <parquet> [N] [workers]"),
]
BY_NAME = {c.name: c for c in COMMANDS}
HELP_FLAGS = ("-h", "--help")


# --------------------------------------------------------------------------- help
def script_docstring(cmd):
    """Module docstring of the script, read statically (no import, no side effects)."""
    try:
        with open(cmd.script, encoding="utf-8") as fh:
            return ast.get_docstring(ast.parse(fh.read())) or ""
    except Exception as e:  # pragma: no cover - only if the checkout is broken
        return f"(docstring unavailable: {e})"


def build_parser():
    epilog = ["commands (each runs koor/<script>.py unchanged):"]
    for c in COMMANDS:
        epilog.append(f"  {c.name:<17} {c.summary}")
    epilog.append(f"  {'config':<17} 打印生效的配置 (koor.toml + KOOR_* 环境变量)")
    epilog.append("")
    epilog.append("run 'koor <command> --help' for the script's own usage and options;")
    epilog.append("everything after <command> is passed to the script verbatim.")
    p = argparse.ArgumentParser(
        prog="koor",
        description="ComplexCAD / koor toolchain: quantised-coordinate CadQuery "
                    "conversion, drawing generation and modelling-precision evaluation.",
        epilog="\n".join(epilog),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version=f"koor {__version__}")
    p.add_argument("--config", metavar="PATH",
                   help="TOML config file (default: $KOOR_CONFIG, ./koor.toml, "
                        "<1m_Convert>/koor.toml)")
    p.add_argument("--log-level", metavar="LEVEL",
                   help="CLI log level (default from config, else INFO)")
    p.add_argument("--log-file", metavar="PATH",
                   help="also append CLI log records to this file")
    p.add_argument("command", nargs="?", choices=list(BY_NAME) + ["config"],
                   metavar="<command>")
    p.add_argument("args", nargs=argparse.REMAINDER, metavar="...",
                   help="arguments passed verbatim to the script")
    return p


def print_command_help(cmd, out=None):
    """``koor <cmd> --help``: static docstring, then the script's own argparse
    help when it has one (imported lazily; a missing optional dependency only
    downgrades this second part to a note)."""
    out = out or sys.stdout
    rel = os.path.relpath(cmd.script, os.path.dirname(HERE))
    print(f"koor {cmd.name}  ->  python {rel} [args...]", file=out)
    print(f"  {cmd.summary}\n", file=out)
    doc = script_docstring(cmd).strip()
    if doc:
        print(doc + "\n", file=out)
    if cmd.argparse:
        print("script options:", file=out)
        try:
            mod = importlib.import_module("koor." + cmd.module)
        except Exception as e:
            print(f"  (unavailable in this environment: {type(e).__name__}: {e})",
                  file=out)
            return
        saved = sys.argv
        sys.argv = [cmd.script, "--help"]
        try:
            mod.main()
        except SystemExit:
            pass
        finally:
            sys.argv = saved
    else:
        print("script options: positional arguments as described above "
              "(the script parses sys.argv itself; no --options).", file=out)


# --------------------------------------------------------------------------- run
def _has_option(args, opt):
    return any(a == opt or a.startswith(opt + "=") for a in args)


def apply_config_passthrough(cmd, args, cfg, log):
    """Forward explicitly configured values to options the script already has,
    unless the option is on the command line."""
    args = list(args)
    for opt, fld in cmd.passthrough:
        val = getattr(cfg, fld, "")
        if cfg.explicit(fld) and val and not _has_option(args, opt):
            log.info("config[%s] (%s) -> %s %s", fld, cfg.sources[fld], opt, val)
            args = [opt, val] + args
    return args


def run_command(cmd, args, cfg, log):
    """Run the script's entry point in-process with ``sys.argv`` set as if the
    script had been started directly. Returns the exit status."""
    args = apply_config_passthrough(cmd, args, cfg, log)
    argv = [cmd.script] + args
    log.info("run %s -> %s %s", cmd.name, os.path.basename(cmd.script),
             " ".join(args) if args else "(no args)")
    saved = sys.argv
    sys.argv = argv
    t0 = time.time()
    status = 0
    try:
        if cmd.mode == "runpy":
            runpy.run_module("koor." + cmd.module, run_name="__main__", alter_sys=True)
        else:
            mod = importlib.import_module("koor." + cmd.module)
            rv = mod.main()
            status = 0 if rv is None or rv is True else int(rv)
    except SystemExit as e:                     # argparse errors / explicit exits
        code = e.code
        status = 0 if code is None else (code if isinstance(code, int) else 1)
        if status:
            log.error("%s exited with status %s", cmd.name, code)
    except KeyboardInterrupt:
        log.warning("%s interrupted", cmd.name)
        status = 130
    except Exception:
        log.exception("%s failed", cmd.name)
        status = 1
    finally:
        sys.argv = saved
    log.info("done %s status=%d in %.1fs", cmd.name, status, time.time() - t0)
    return status


def main(argv=None):
    parser = build_parser()
    ns = parser.parse_args(sys.argv[1:] if argv is None else list(argv))
    if not ns.command:
        parser.print_help()
        return 0

    if ns.command == "config":
        cfg = load_config(ns.config)
        print(cfg.describe())
        return 0

    cmd = BY_NAME[ns.command]
    if any(a in HELP_FLAGS for a in ns.args):
        print_command_help(cmd)
        return 0

    cfg = load_config(ns.config)
    log = setup_logging(ns.log_level or cfg.log_level, ns.log_file or cfg.log_file or None)
    log.debug("koor %s  config=%s", __version__, cfg.config_file or "(defaults)")
    return run_command(cmd, ns.args, cfg, log)


if __name__ == "__main__":  # pragma: no cover - `python -m koor.cli`
    sys.exit(main())
