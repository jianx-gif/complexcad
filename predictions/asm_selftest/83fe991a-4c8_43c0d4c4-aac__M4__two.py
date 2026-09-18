_t = gp_Trsf()
_t.SetValues(1, 0, 0, -5, 0, 1, 0, -45, 0, 0, 1, 30)
_sb = baseB.val() if hasattr(baseB, 'val') else baseB
_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb
baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())
parts = [baseA, baseB]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(-35, -45, 14), seat=26, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 46, 0), axis=(0, 0, 1), point=(-35, -45, 14), seat=26.9, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(-35, -45, 14), seat=-14, flip=True))
