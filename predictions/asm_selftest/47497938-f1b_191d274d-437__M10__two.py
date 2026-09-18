_t = gp_Trsf()
_t.SetValues(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 20)
_sb = baseB.val() if hasattr(baseB, 'val') else baseB
_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb
baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())
parts = [baseA, baseB]
parts.append(place(fastener("washer", 'M10', 0), axis=(0, 0, 1), point=(0, 0, 10), seat=18, flip=False))
parts.append(place(fastener("screw", 'M10-1.5', 40, 0), axis=(0, 0, 1), point=(0, 0, 10), seat=20.2, flip=False))
parts.append(place(fastener("nut", 'M10-1.5', 'M10', 0), axis=(0, 0, 1), point=(0, 0, 10), seat=-10, flip=True))
