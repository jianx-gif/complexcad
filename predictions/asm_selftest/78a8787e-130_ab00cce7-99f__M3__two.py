_t = gp_Trsf()
_t.SetValues(1, 0, 0, 20, 0, 1, 0, -5, 0, 0, 1, 22.5)
_sb = baseB.val() if hasattr(baseB, 'val') else baseB
_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb
baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())
parts = [baseA, baseB]
parts.append(place(fastener("washer", 'M3', 0), axis=(0, 0, 1), point=(0, -15, 10), seat=15, flip=False))
parts.append(place(fastener("screw", 'M3-0.5', 30, 0), axis=(0, 0, 1), point=(0, -15, 10), seat=15.55, flip=False))
parts.append(place(fastener("nut", 'M3-0.5', 'M3', 0), axis=(0, 0, 1), point=(0, -15, 10), seat=-10, flip=True))
