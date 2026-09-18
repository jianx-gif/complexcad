"""Make open3d importable from the isolated pylib folder without the plotly/dash web stack
(only open3d.visualization.Visualizer offscreen rendering is needed, as in cadrille dataset.py)."""
import sys, types, os
PYLIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pylib')
if PYLIB not in sys.path:
    sys.path.insert(0, PYLIB)
for name in ['plotly', 'plotly.graph_objects', 'dash', 'dash.html', 'dash.dcc']:
    if name not in sys.modules:
        sys.modules[name] = types.ModuleType(name)
sys.modules['dash'].html = sys.modules['dash.html']
sys.modules['dash'].dcc = sys.modules['dash.dcc']
sys.modules['dash'].Dash = object
sys.modules['plotly'].graph_objects = sys.modules['plotly.graph_objects']
import open3d  # noqa: E402,F401
