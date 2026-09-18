_t = gp_Trsf()
_t.SetValues(1, 0, 0, -15, 0, 1, 0, -53.981, 0, 0, 1, 8)
_sb = baseB.val() if hasattr(baseB, 'val') else baseB
_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb
baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())
parts = [baseA, baseB]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(-15, -25.981, 4), seat=12, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 22, 0), axis=(0, 0, 1), point=(-15, -25.981, 4), seat=12.9, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(-15, -25.981, 4), seat=-4, flip=True))
