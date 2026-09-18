_t = gp_Trsf()
_t.SetValues(1, 0, 0, 0, 0, 1, 0, 30, 0, 0, 1, 32.5)
_sb = baseB.val() if hasattr(baseB, 'val') else baseB
_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb
baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())
parts = [baseA, baseB]
parts.append(place(fastener("washer", 'M3', 0), axis=(0, 0, 1), point=(-20, 20, 21.698), seat=13.302, flip=False))
parts.append(place(fastener("screw", 'M3-0.5', 26, 0), axis=(0, 0, 1), point=(-20, 20, 21.698), seat=13.852, flip=False))
parts.append(place(fastener("nut", 'M3-0.5', 'M3', 0), axis=(0, 0, 1), point=(-20, 20, 21.698), seat=-7.302, flip=True))
