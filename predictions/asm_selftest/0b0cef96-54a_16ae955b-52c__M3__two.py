_t = gp_Trsf()
_t.SetValues(1, 0, 0, -10, 0, 1, 0, -17.321, 0, 0, 1, 13)
_sb = baseB.val() if hasattr(baseB, 'val') else baseB
_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb
baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())
parts = [baseA, baseB]
parts.append(place(fastener("washer", 'M3', 0), axis=(0, 0, 1), point=(-10, -17.321, 6.5), seat=14.5, flip=False))
parts.append(place(fastener("screw", 'M3-0.5', 26, 0), axis=(0, 0, 1), point=(-10, -17.321, 6.5), seat=15.05, flip=False))
parts.append(place(fastener("nut", 'M3-0.5', 'M3', 0), axis=(0, 0, 1), point=(-10, -17.321, 6.5), seat=-6.5, flip=True))
