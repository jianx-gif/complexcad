_t = gp_Trsf()
_t.SetValues(1, 0, 0, -45, 0, 0, -1, -20, 0, 1, 0, 25)
_sb = baseB.val() if hasattr(baseB, 'val') else baseB
_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb
baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())
parts = [baseA, baseB]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, -1, 0), point=(-15, -18.5, 25), seat=5.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 50, 0), axis=(0, -1, 0), point=(-15, -18.5, 25), seat=6.4, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, -1, 0), point=(-15, -18.5, 25), seat=-38.5, flip=True))
