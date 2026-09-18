_t = gp_Trsf()
_t.SetValues(1, 0, 0, 15, 0, -1, 0, 40, 0, 0, -1, 40)
_sb = baseB.val() if hasattr(baseB, 'val') else baseB
_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb
baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())
parts = [baseA, baseB]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 1, 0), point=(0, -19, 15), seat=79, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 86, 0), axis=(0, 1, 0), point=(0, -19, 15), seat=79.9, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 1, 0), point=(0, -19, 15), seat=-1, flip=True))
