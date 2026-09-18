_t = gp_Trsf()
_t.SetValues(1, 0, 0, -50, 0, 1, 0, -40, 0, 0, 1, 5)
_sb = baseB.val() if hasattr(baseB, 'val') else baseB
_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb
baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())
parts = [baseA, baseB]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(-45, -25, 2.5), seat=8.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 18, 0), axis=(0, 0, 1), point=(-45, -25, 2.5), seat=9.4, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(-45, -25, 2.5), seat=-2.5, flip=True))
