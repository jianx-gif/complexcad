"""Optional configuration for the ``koor`` command line.

Precedence, highest first:

1. environment variables ``KOOR_*`` (see :data:`FIELDS`),
2. a TOML file: ``--config PATH``, else ``$KOOR_CONFIG``, else ``./koor.toml``,
   else ``<1m_Convert>/koor.toml`` (``koor.example.toml`` next to it documents
   every key),
3. built-in defaults derived from the checkout layout -- the same
   ``HERE / PARENT / ROOT`` directories the scripts compute from ``__file__``.

The thesis scripts never read this file and their own defaults are untouched.
:mod:`koor.cli` forwards a value only to a script option that already exists
(``convert --outdir``, ``recover --dir``, ``peek --dir``,
``eval-predictions --names-file``, ``adapt-cadrecode --names-file``) and only
when the key was *explicitly* set in the file or the environment, so with no
config present ``koor <cmd> ...`` behaves exactly like
``python koor/<script>.py ...``.
"""
import os
from dataclasses import dataclass, field

KOOR_DIR = os.path.dirname(os.path.abspath(__file__))   # .../1m_Convert/koor  (HERE in the scripts)
PROJECT_DIR = os.path.dirname(KOOR_DIR)                 # .../1m_Convert       (PARENT)
DEFAULT_ROOT = os.path.dirname(PROJECT_DIR)             # .../data             (ROOT)
DEFAULT_CONFIG_NAME = "koor.toml"
ENV_CONFIG = "KOOR_CONFIG"

# (field, toml section, toml key, environment variable, default(root, project), is_path)
FIELDS = [
    ("root", "paths", "root", "KOOR_ROOT",
     lambda r, p: r, True),
    ("output_dir", "paths", "output_dir", "KOOR_OUTPUT_DIR",
     lambda r, p: os.path.join(r, "output"), True),
    ("splits_dir", "paths", "splits_dir", "KOOR_SPLITS_DIR",
     lambda r, p: os.path.join(r, "splits"), True),
    ("predictions_dir", "paths", "predictions_dir", "KOOR_PREDICTIONS_DIR",
     lambda r, p: os.path.join(r, "predictions"), True),
    ("report_dir", "paths", "report_dir", "KOOR_REPORT_DIR",
     lambda r, p: os.path.join(p, "precision_report"), True),
    ("names_file", "paths", "names_file", "KOOR_NAMES_FILE",
     lambda r, p: "", True),
    ("convert_outdir", "convert", "outdir", "KOOR_CONVERT_OUTDIR",
     lambda r, p: "", True),
    ("convert_train_dir", "convert", "train_dir", "KOOR_CONVERT_TRAIN_DIR",
     lambda r, p: "", True),
    ("log_level", "logging", "level", "KOOR_LOG_LEVEL",
     lambda r, p: "INFO", False),
    ("log_file", "logging", "file", "KOOR_LOG_FILE",
     lambda r, p: "", True),
]
FIELD_NAMES = [f[0] for f in FIELDS]
ENV_VARS = {f[0]: f[3] for f in FIELDS}


@dataclass
class KoorConfig:
    root: str = DEFAULT_ROOT
    output_dir: str = ""
    splits_dir: str = ""
    predictions_dir: str = ""
    report_dir: str = ""
    names_file: str = ""
    convert_outdir: str = ""
    convert_train_dir: str = ""
    log_level: str = "INFO"
    log_file: str = ""
    config_file: str = ""                        # the TOML file that was read, if any
    sources: dict = field(default_factory=dict)  # field -> "default" | "file" | "env"

    def explicit(self, name):
        """True if ``name`` was set in the config file or the environment."""
        return self.sources.get(name) in ("file", "env")

    def as_dict(self):
        return {n: getattr(self, n) for n in FIELD_NAMES}

    def describe(self):
        """Human-readable dump used by ``koor config``."""
        lines = [f"config_file        = {self.config_file or '(none)'}"]
        for n in FIELD_NAMES:
            v = getattr(self, n)
            lines.append(f"{n:<18} = {v!r:<58} # {self.sources.get(n, 'default')}"
                         f" ({ENV_VARS[n]})")
        return "\n".join(lines)


# --------------------------------------------------------------------------- TOML
def _parse_toml_minimal(text):
    """Tiny fallback parser for the flat ``[section]`` / ``key = value`` subset
    used by koor.toml, for when neither ``tomllib`` (3.11+) nor ``tomli`` is
    importable. Supports comments, quoted strings, ints, floats and booleans."""
    data = {}
    cur = data
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            sec = line[1:-1].strip().strip('"').strip("'")
            cur = data.setdefault(sec, {})
            continue
        if "=" not in line:
            raise ValueError(f"cannot parse config line: {raw!r}")
        k, v = line.split("=", 1)
        k = k.strip().strip('"').strip("'")
        v = v.strip()
        if v[:1] in ("'", '"'):
            q = v[0]
            end = v.find(q, 1)
            while end != -1 and q == '"' and v[end - 1] == "\\":
                end = v.find(q, end + 1)
            if end == -1:
                raise ValueError(f"unterminated string in config line: {raw!r}")
            s = v[1:end]
            val = s.encode("utf-8").decode("unicode_escape") if q == '"' else s
        else:
            v = v.split("#", 1)[0].strip()
            if v in ("true", "false"):
                val = v == "true"
            else:
                try:
                    val = int(v)
                except ValueError:
                    val = float(v)
        cur[k] = val
    return data


def _load_toml(path):
    text = open(path, "rb").read().decode("utf-8")
    try:
        import tomllib                      # Python >= 3.11
    except ImportError:
        try:
            import tomli as tomllib         # backport (declared dependency on 3.10)
        except ImportError:
            tomllib = None
    if tomllib is not None:
        return tomllib.loads(text)
    return _parse_toml_minimal(text)


def find_config_file(path=None, env=None, cwd=None):
    """Resolve which config file to use, or None. See the module docstring."""
    env = os.environ if env is None else env
    cwd = cwd or os.getcwd()
    if path:
        p = os.path.expanduser(path)
        if not os.path.isfile(p):
            raise FileNotFoundError(f"config file not found: {path}")
        return os.path.abspath(p)
    candidates = []
    if env.get(ENV_CONFIG):
        candidates.append(env[ENV_CONFIG])
    candidates.append(os.path.join(cwd, DEFAULT_CONFIG_NAME))
    candidates.append(os.path.join(PROJECT_DIR, DEFAULT_CONFIG_NAME))
    for c in candidates:
        c = os.path.expanduser(c)
        if os.path.isfile(c):
            return os.path.abspath(c)
    return None


def _norm_path(v, base=None):
    v = os.path.expanduser(str(v))
    if base and not os.path.isabs(v):
        v = os.path.join(base, v)
    return os.path.normpath(v)


def load_config(path=None, env=None, cwd=None):
    """Build a :class:`KoorConfig` from defaults, an optional TOML file and the
    environment. ``env`` defaults to ``os.environ`` (pass a dict in tests)."""
    env = os.environ if env is None else env
    cfg_path = find_config_file(path, env, cwd)
    filedata = _load_toml(cfg_path) if cfg_path else {}
    base = os.path.dirname(cfg_path) if cfg_path else None

    def from_file(section, key):
        sec = filedata.get(section)
        if isinstance(sec, dict) and key in sec:
            return sec[key]
        return None

    values, sources = {}, {}
    # "root" is first in FIELDS: the other path defaults derive from it.
    for name, section, key, envvar, default, is_path in FIELDS:
        root = values.get("root", DEFAULT_ROOT)
        fv = from_file(section, key)
        if env.get(envvar, "") != "":
            v, src = env[envvar], "env"
            if is_path:
                v = _norm_path(v)
        elif fv is not None:
            v, src = fv, "file"
            if is_path and v != "":
                v = _norm_path(v, base)
        else:
            v, src = default(root, PROJECT_DIR), "default"
        values[name] = v
        sources[name] = src
    values["log_level"] = str(values["log_level"]).upper()
    return KoorConfig(config_file=cfg_path or "", sources=sources, **values)
