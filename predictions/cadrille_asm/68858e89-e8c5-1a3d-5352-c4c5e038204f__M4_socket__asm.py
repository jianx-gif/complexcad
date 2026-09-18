parts = [base]
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-25, -8, 4), seat=12, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 14, 0), axis=(0, 0, 1), point=(-25, -8, 4), seat=12.9, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(-25, -8, 4), seat=-4, flip=True))
