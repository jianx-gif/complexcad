_t = gp_Trsf()
_t.SetValues(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 15)
_sb = baseB.val() if hasattr(baseB, 'val') else baseB
_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb
baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())
parts = [baseA, baseB]
parts.append(place(fastener("washer", 'M10', 0), axis=(0, 0, 1), point=(0, 0, 7.1), seat=15.9, flip=False))
parts.append(place(fastener("screw", 'M10-1.5', 34, 0), axis=(0, 0, 1), point=(0, 0, 7.1), seat=18.1, flip=False))
parts.append(place(fastener("nut", 'M10-1.5', 'M10', 0), axis=(0, 0, 1), point=(0, 0, 7.1), seat=-7.1, flip=True))
