_t = gp_Trsf()
_t.SetValues(1, 0, 0, 0, 0, 1, 0, -8, 0, 0, 1, 27.5)
_sb = baseB.val() if hasattr(baseB, 'val') else baseB
_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb
baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())
parts = [baseA, baseB]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(-10, 0, 12.5), seat=17.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 36, 0), axis=(0, 0, 1), point=(-10, 0, 12.5), seat=18.4, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(-10, 0, 12.5), seat=-12.5, flip=True))
