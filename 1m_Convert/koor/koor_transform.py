"""Zero-To-CAD CadQuery 程序的坐标/参数量化转换。

把所有"长度类"建模参数乘以全局 scale(默认100) 并取整到 [-CLAMP, CLAMP]
(默认 CLAMP=10000)，从而映射到 1-10000 的整数坐标网格；保留绝对比例。
角度(angle/deg)、个数(count/nSides)、比例因子(/2, *0.5)、负号方向、
字符串选择器('>Z','XY') 一律保持不变。

核心思路: "语义类型"沿表达式向下传播。
  L=LENGTH 长度(可缩放)  A=ANGLE 角度  C=COUNT 个数  R=RATIO 比例因子  U=UNKNOWN
只有在 L 上下文里的"叶子数字字面量"才会被缩放。
"""
import ast

L, A, C, R, U = "L", "A", "C", "R", "U"

# ---- 函数 -> 位置参数语义 ---------------------------------------------------
# 所有位置参数都是长度的方法
SPATIAL_ALL = {
    "box", "rect", "circle", "ellipse", "ellipseArc", "slot2D", "extrude",
    "cutBlind", "hole", "cylinder", "sphere", "fillet", "chamfer", "shell",
    "offset2D", "line", "lineTo", "moveTo", "vLine", "hLine", "vLineTo",
    "hLineTo", "center", "translate", "polyline", "threePointArc",
    "tangentArcPoint", "sagittaArc", "pushPoints", "wedge", "rect2D",
    "radiusArc", "box2D", "spline", "bezier", "interpPolyline",
}
# 特殊位置参数表 (方法 -> 各位置参数的 kind 列表; 超出部分用最后一个/默认 L)
SPECIAL_POS = {
    "polygon":      [C, L],                  # nSides, diameter
    "rarray":       [L, L, C, C],            # xSpacing, ySpacing, xCount, yCount
    "polarArray":   [L, C, A, A],            # radius, count, startAngle, angle
    "cboreHole":    [L, L, L, L],            # diameter, cboreDiameter, cboreDepth, depth
    "cskHole":      [L, L, A, L],            # diameter, cskDiameter, cskAngle, depth
    "cbore":        [L, L, L],
    "revolve":      [A, L, L],               # angleDegrees, axisStart, axisEnd
    "rotate":       [L, L, A],               # axisStart, axisEnd, angleDegrees
    "rotateAboutCenter": [L, A],             # axisEndPoint, angleDegrees
    "circle2D":     [L],
}
# 透传函数: 返回值类型 = 调用处期望类型(把上下文 kind 传给参数)
PASSTHROUGH = {"abs", "min", "max", "round", "float", "fabs"}
# 角度域函数: 参数当作角度(不缩放)
ANGLE_FUNCS = {"radians", "degrees", "sin", "cos", "tan", "asin", "acos", "atan", "atan2"}
# 个数域函数: 参数当作个数/比例(不缩放)
COUNT_FUNCS = {"range", "int", "len", "enumerate"}
# 纯比例函数
RATIO_FUNCS = {"sqrt", "pow", "exp", "log"}
# namespace 容器: kwargs 按名字分类
NS_FUNCS = {"Measures", "SimpleNamespace", "dict", "Namespace"}

# ---- kwarg 名 -> 语义 -------------------------------------------------------
KW_ANGLE = {"angle", "startAngle", "stopAngle", "angleDegrees", "angle1",
            "angle2", "cskAngle", "endAngle", "sweep", "twist"}
KW_COUNT = {"count", "xCount", "yCount", "nSides", "n", "num", "segments",
            "nr", "numbed"}
KW_SKIP = {"centerOption", "centered", "combine", "mode", "forConstruction",
           "clean", "makeSolid", "both", "transition", "name", "tag", "axis",
           "origin", "normal", "xDir", "invert", "positive", "kind", "until"}


def _is_angle_name(n):
    """精确判断角度: 避免 'radius' 被误判为 radians。"""
    return ("angle" in n or "degree" in n or n.endswith("_deg") or "_deg_" in n
            or n.startswith("deg_") or "radian" in n or n.endswith("_rad")
            or "_rad_" in n)


def kw_kind(name):
    if name in KW_SKIP:
        return None
    if name in KW_ANGLE:
        return A
    if name in KW_COUNT:
        return C
    n = name.lower()
    if _is_ratio_name(n):
        return R
    if _is_angle_name(n):
        return A
    if any(k in n for k in ("count", "num", "nsides", "sides", "segment", "teeth")):
        return C
    return L


RATIO_NAME = ("factor", "ratio", "fraction", "frac", "percent", "pct",
              "coeff", "coef", "multiplier", "aspect", "gain")


def _is_ratio_name(n):
    return any(k in n for k in RATIO_NAME)


def var_kind(name):
    """顶层赋值变量名 -> 语义。"""
    n = name.lower()
    if _is_ratio_name(n):
        return R
    if _is_angle_name(n):
        return A
    if (("count" in n) or n.startswith("n_") or n.endswith("_n") or
            "nsides" in n or n.endswith("sides") or "segment" in n or
            "teeth" in n or "_num" in n or n.startswith("num")):
        return C
    return L


# ---------------------------------------------------------------------------
class Scaler:
    def __init__(self, scale=100, clamp=10000, collect=False, min_mag=0):
        self.scale = scale
        self.clamp = clamp
        self.collect = collect          # True: 只收集长度字面量, 不改 AST
        self.min_mag = min_mag          # >0: 非零值取整后至少保留这么多单位(防退化成0)
        self.values = []                # collect 模式下记录 |length literal|
        self.n_scaled = 0
        self.n_clamped = 0
        self.unknown_methods = {}

    def quant(self, v):
        q = int(round(v * self.scale))
        # 非零长度被取整成 0 -> 保留最小幅度(避免 0 高度/0 半径退化)
        if self.min_mag and q == 0 and v != 0:
            q = self.min_mag if v > 0 else -self.min_mag
        if q > self.clamp:
            q = self.clamp
            self.n_clamped += 1
        elif q < -self.clamp:
            q = -self.clamp
            self.n_clamped += 1
        return q

    # ---- 表达式: 在 kind 上下文里递归缩放 -------------------------------
    def expr(self, node, kind):
        if node is None:
            return
        # 叶子数字
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) \
                and not isinstance(node.value, bool):
            if kind == L:
                if self.collect:
                    if node.value != 0:
                        self.values.append(abs(node.value))
                else:
                    node.value = self.quant(node.value)
                    self.n_scaled += 1
            return
        # -x / +x : 符号保留, 操作数继承 kind
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            self.expr(node.operand, kind)
            return
        if isinstance(node, ast.BinOp):
            op = node.op
            if isinstance(op, (ast.Add, ast.Sub)):           # 加减: 两侧都是同量纲
                self.expr(node.left, kind)
                self.expr(node.right, kind)
            elif isinstance(op, (ast.Mult, ast.MatMult)):    # 乘: 两侧字面量都是无量纲因子
                self.expr(node.left, R)                       # (width*0.5, (i+1)*spacing
                self.expr(node.right, R)                       #  里的 0.5/1 都不缩放)
            elif isinstance(op, (ast.Div, ast.FloorDiv, ast.Mod, ast.Pow)):
                self.expr(node.left, kind)                    # 分子保留 kind(可含长度)
                self.expr(node.right, R)                       # 分母=比例, 不缩放
            else:
                self.expr(node.left, kind)
                self.expr(node.right, kind)
            return
        if isinstance(node, (ast.Tuple, ast.List, ast.Set)):  # 坐标容器: 元素继承 kind
            for e in node.elts:
                self.expr(e, kind)
            return
        if isinstance(node, ast.Call):
            self.call(node, kind)
            return
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
            self.expr(node.elt, kind)
            for g in node.generators:
                self.expr(g.iter, U)
            return
        if isinstance(node, ast.DictComp):
            self.expr(node.value, kind)
            for g in node.generators:
                self.expr(g.iter, U)
            return
        if isinstance(node, ast.IfExp):
            self.expr(node.body, kind)
            self.expr(node.orelse, kind)
            return
        if isinstance(node, ast.Dict):
            for v in node.values:
                self.expr(v, kind)
            return
        if isinstance(node, ast.Subscript):
            self.expr(node.value, U)
            return
        # Name / Attribute / Str 等: 不动 (变量在定义处缩放)
        if isinstance(node, (ast.Name, ast.Attribute)):
            return
        # 兜底: 递归子节点, 传 U(不缩放)
        for child in ast.iter_child_nodes(node):
            self.expr(child, U)

    @staticmethod
    def _is_num(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) \
                and not isinstance(n.value, bool):
            return True
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            return Scaler._is_num(n.operand)
        return False

    # ---- 函数调用 ------------------------------------------------------
    def call(self, node, ctx_kind):
        f = node.func
        name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
        # 先递归进入被调用对象 (链式调用 a.b().c() 里的字面量)
        if isinstance(f, ast.Attribute):
            self.expr(f.value, U)

        # namespace 容器: kwargs 按名字
        if name in NS_FUNCS:
            for a in node.args:
                self.expr(a, L)
            for kw in node.keywords:
                k = kw_kind(kw.arg) if kw.arg else L
                if k is not None:
                    self.expr(kw.value, k)
            return
        if name in PASSTHROUGH:
            for a in node.args:
                self.expr(a, ctx_kind)
            self._kwargs(node)
            return
        if name in ANGLE_FUNCS:
            for a in node.args:
                self.expr(a, A)
            self._kwargs(node)
            return
        if name in COUNT_FUNCS:
            for a in node.args:
                self.expr(a, C)
            self._kwargs(node)
            return
        if name in RATIO_FUNCS:
            for a in node.args:
                self.expr(a, R)
            self._kwargs(node)
            return

        if name in SPECIAL_POS:
            kinds = SPECIAL_POS[name]
            for i, a in enumerate(node.args):
                k = kinds[i] if i < len(kinds) else kinds[-1]
                self.expr(a, k)
            self._kwargs(node)
            return
        if name in SPATIAL_ALL:
            for a in node.args:
                self.expr(a, L)
            self._kwargs(node)
            return

        # 未知方法: 位置参数默认按长度(几何代码), 记录以便复核
        if name and node.args:
            cnt = sum(1 for a in ast.walk(node) if isinstance(a, ast.Constant)
                      and isinstance(a.value, (int, float)) and not isinstance(a.value, bool))
            if cnt:
                self.unknown_methods[name] = self.unknown_methods.get(name, 0) + 1
        for a in node.args:
            self.expr(a, L)
        self._kwargs(node)

    def _kwargs(self, node):
        for kw in node.keywords:
            if kw.arg is None:                       # **kwargs
                self.expr(kw.value, U)
                continue
            k = kw_kind(kw.arg)
            if k is not None:
                self.expr(kw.value, k)

    # ---- 语句 ----------------------------------------------------------
    def stmt(self, node):
        if isinstance(node, ast.Assign):
            kinds = []
            for tgt in node.targets:
                if isinstance(tgt, ast.Name):
                    kinds.append(var_kind(tgt.id))
                elif isinstance(tgt, (ast.Tuple, ast.List)):
                    kinds.append(L)
                else:
                    kinds.append(L)
            self.expr(node.value, kinds[0] if kinds else L)
            return
        if isinstance(node, ast.AnnAssign) and node.value is not None:
            k = var_kind(node.target.id) if isinstance(node.target, ast.Name) else L
            self.expr(node.value, k)
            return
        if isinstance(node, ast.AugAssign):
            k = var_kind(node.target.id) if isinstance(node.target, ast.Name) else L
            self.expr(node.value, k)
            return
        if isinstance(node, ast.Expr):
            self.expr(node.value, U)
            return
        if isinstance(node, ast.Return) and node.value is not None:
            self.expr(node.value, L)
            return
        if isinstance(node, ast.For):
            self.expr(node.iter, U)
            for s in node.body:
                self.stmt(s)
            for s in node.orelse:
                self.stmt(s)
            return
        if isinstance(node, (ast.If, ast.While)):
            for s in node.body:
                self.stmt(s)
            for s in node.orelse:
                self.stmt(s)
            return
        if isinstance(node, ast.With):
            for item in node.items:
                self.expr(item.context_expr, U)
            for s in node.body:
                self.stmt(s)
            return
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for s in node.body:
                self.stmt(s)
            return
        # 其它语句: 递归子语句
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.stmt):
                self.stmt(child)


def scale_code(src, scale=100, clamp=10000, min_mag=0):
    """返回 (新代码字符串, stats dict)。min_mag>0: 非零长度取整后至少保留这么多单位。
    解析失败抛 SyntaxError。"""
    tree = ast.parse(src)
    sc = Scaler(scale=scale, clamp=clamp, min_mag=min_mag)
    for node in tree.body:
        sc.stmt(node)
    ast.fix_missing_locations(tree)
    new_src = ast.unparse(tree)
    stats = {"n_scaled": sc.n_scaled, "n_clamped": sc.n_clamped,
             "unknown_methods": sc.unknown_methods}
    return new_src, stats


def collect_lengths(src):
    """返回该程序里所有"会被缩放的长度字面量"的绝对值列表(用同一套分类)。"""
    tree = ast.parse(src)
    sc = Scaler(collect=True)
    for node in tree.body:
        sc.stmt(node)
    return sc.values


if __name__ == "__main__":
    import sys
    src = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
    out, st = scale_code(src)
    sys.stderr.write(f"# stats: {st}\n")
    print(out)
